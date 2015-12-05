from itertools import chain

from django.shortcuts import get_object_or_404, Http404
from django.utils.crypto import get_random_string

from rest_framework import filters, generics, mixins, permissions, status
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import Follower, MyUser
from comments.models import Comment
from hashtags.models import Hashtag
from notifications.models import Notification
from notifications.signals import notify
from photos.models import Category, Photo
from .account_serializers import (AccountCreateSerializer, FollowerSerializer,
                                  MyUserSerializer)
from .auth_serializers import (PasswordResetSerializer,
                               PasswordResetConfirmSerializer,
                               PasswordChangeSerializer)
from .comment_serializers import (CommentCreateSerializer, CommentSerializer,
                                  CommentUpdateSerializer)
from .hashtag_serializers import HashtagSerializer
from .mixins import DefaultsMixin
from .notification_serializers import NotificationSerializer
from .pagination import (AccountPagination, CommentPagination,
                         HashtagPagination, NotificationPagination,
                         PhotoPagination)
from .permissions import (IsCreatorOrReadOnly, IsOwnerOrReadOnly,
                          MyUserIsOwnerOrReadOnly)
from .photo_serializers import (CategorySerializer, PhotoCreateSerializer,
                                PhotoSerializer)
from .search_serializers import SearchMyUserSerializer

# Create your views here.


class APIHomeView(DefaultsMixin, APIView):
    def get(self, request, format=None):
        data = {
            'authentication': {
                'login': api_reverse('auth_login_api', request=request),
                'password_reset': api_reverse('api:rest_password_reset',
                                              request=request),
                'password_change': api_reverse('api:rest_password_change',
                                               request=request)
            },
            'accounts': {
                'count': MyUser.objects.all().count(),
                'url': api_reverse('api:user_account_list_api', request=request),
                'create_url': api_reverse('api:account_create_api',
                                          request=request),
                'edit_profile_url': api_reverse(
                    'api:user_account_detail_api', request=request,
                    kwargs={'username': request.user.username})
            },
            'categories': {
                'url': api_reverse('api:category_list_api', request=request),
            },
            'comments': {
                'url': api_reverse('api:comment_list_api', request=request),
                'create_url': api_reverse('api:comment_create_api',
                                          request=request),
            },
            'hashtags': {
                'count': Hashtag.objects.all().count(),
                'url': api_reverse('api:hashtag_list_api', request=request),
            },
            'homepage': {
                'url': api_reverse('api:homepage_api', request=request),
            },
            'notifications': {
                'url': api_reverse('api:notification_list_api', request=request),
            },
            'photos': {
                'count': Photo.objects.all().count(),
                'url': api_reverse('api:photo_list_api', request=request),
                'create_url': api_reverse('api:photo_create_api', request=request),
            },
            'search': {
                'url': api_reverse('api:search_api', request=request),
                'help_text': "add '?q=searched_parameter' to the "
                             "end of the url to display results"
            },
            'timeline': {
                'url': api_reverse('api:timeline_api', request=request),
            },
        }
        return RestResponse(data)


class HomepageAPIView(DefaultsMixin, generics.ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.most_liked_offset()[:30]


class TimelineAPIView(DefaultsMixin, generics.ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        user = self.request.user
        photos_self = Photo.objects.own(user)

        try:
            follow = Follower.objects.get(user=user)
        except Follower.DoesNotExist:
            follow = None

        if follow:
            photos_following = Photo.objects.following(user)
            return (photos_self | photos_following).distinct()[:250]
        else:
            # Add suggested users
            photos_suggested = Photo.objects.all() \
                .select_related("creator", "category") \
                .exclude(creator=user)[:50]
            photos = chain(photos_self, photos_suggested)
            return photos


# A C C O U N T S
@api_view(['POST'])
def follow_create_api(request, user_pk):
    follower, created = Follower.objects.get_or_create(user=request.user)
    user = get_object_or_404(MyUser, pk=user_pk)
    followed, created = Follower.objects.get_or_create(user=user)

    try:
        user_followed = Follower.objects.get(user=user, followers=follower)
    except Follower.DoesNotExist:
        user_followed = None

    if user_followed:
        followed.followers.remove(follower)
    else:
        followed.followers.add(follower)
        notify.send(
            request.user,
            recipient=user,
            verb='is now supporting you'
        )
    serializer = FollowerSerializer(followed, context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


class AccountCreateAPIView(generics.CreateAPIView):
    serializer_class = AccountCreateSerializer


class MyUserListAPIView(DefaultsMixin, generics.ListAPIView):
    pagination_class = AccountPagination
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()


class MyUserDetailAPIView(generics.RetrieveAPIView,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated, MyUserIsOwnerOrReadOnly]
    serializer_class = MyUserSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        username = self.kwargs["username"]
        obj = get_object_or_404(MyUser, username=username)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# A U T H E N T I C A T I O N
class PasswordResetView(generics.GenericAPIView):
    """
    Calls PasswordResetForm save method
    Accepts the following POST parameters: email
    Returns the success/fail message
    """
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return RestResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return RestResponse(
            {"success": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Password reset e-mail link is confirmed, so this resets the user's password
    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return RestResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return RestResponse(
            {"success": "Password has been reset."})


class PasswordChangeView(generics.GenericAPIView):
    """
    Calls SetPasswordForm save method
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return RestResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return RestResponse({"success": "New password has been saved."})


# C O M M E N T S
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        parent_id = self.request.data.get('parent')
        photo_id = self.request.data.get('photo')
        parent_comment = None

        try:
            photo = Photo.objects.get(id=photo_id)
        except:
            photo = None

        if parent_id is not None:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except:
                parent_comment = None
            if parent_comment is not None and parent_comment.photo is not None:
                photo = parent_comment.photo

        if serializer.is_valid():
            comment_text = self.request.data.get('text')
            if parent_comment is not None:
                # parent comments exists
                new_child_comment = Comment.objects.create_comment(
                    user=self.request.user,
                    path=parent_comment.get_origin,
                    text=comment_text,
                    photo=photo,
                    parent=parent_comment
                )
                affected_users = parent_comment.get_affected_users()
                notify.send(
                    self.request.user,
                    action=new_child_comment,
                    target=parent_comment,
                    recipient=parent_comment.user,
                    affected_users=affected_users,
                    verb='replied to'
                )
            else:
                new_parent_comment = Comment.objects.create_comment(
                    user=request.user,
                    path=request.get_full_path,
                    text=comment_text,
                    photo=photo
                )
                notify.send(
                    self.request.user,
                    action=new_parent_comment,
                    target=new_parent_comment.photo,
                    recipient=photo.creator,
                    verb='commented'
                )
            return RestResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        else:
            return RestResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(DefaultsMixin, generics.ListAPIView):
    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentDetailAPIView(generics.RetrieveAPIView, mixins.DestroyModelMixin):
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CommentUpdateSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.filter(pk__gte=0)
        return queryset

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# H A S H T A G S
class HashtagListAPIView(DefaultsMixin, generics.ListAPIView):
    pagination_class = HashtagPagination
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["tag"]


# N O T I F I C A T I O N S
class NotificationAPIView(DefaultsMixin, generics.ListAPIView):
    pagination_class = NotificationPagination
    serializer_class = NotificationSerializer

    def get_queryset(self):
        notifications = Notification.objects.all_for_user(
            self.request.user)[:50]
        for notification in notifications:
            if notification.recipient == self.request.user:
                notification.read = True
                notification.save()
            else:
                raise Http404
        return notifications


# P H O T O S
@api_view(['POST'])
def like_create_api(request, photo_pk):
    user = request.user
    photo = get_object_or_404(Photo, pk=photo_pk)

    if user in photo.likers.all():
        photo.likers.remove(user)
    else:
        photo.likers.add(user)
        notify.send(
            user,
            action=photo,
            target=photo,
            recipient=photo.creator,
            verb='liked'
        )
    serializer = PhotoSerializer(photo, context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


class PhotoCreateAPIView(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoCreateSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user,
                        slug=get_random_string(length=10),
                        photo=self.request.data.get('photo'))


class PhotoListAPIView(DefaultsMixin, generics.ListAPIView):
    pagination_class = PhotoPagination
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["description"]
    ordering_fields = ["created", "modified"]


class PhotoDetailAPIView(generics.RetrieveAPIView,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
    serializer_class = PhotoSerializer

    def get_object(self):
        cat_slug = self.kwargs["cat_slug"]
        photo_slug = self.kwargs["photo_slug"]
        category = get_object_or_404(Category, slug=cat_slug)
        obj = get_object_or_404(Photo, category=category, slug=photo_slug)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CategoryListAPIView(DefaultsMixin, generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.most_posts()


class CategoryDetailAPIView(DefaultsMixin, generics.RetrieveAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Category, slug=slug)
        return obj


# S E A R C H
class SearchListAPIView(DefaultsMixin, generics.ListAPIView):
    serializer_class = SearchMyUserSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    # '^' Starts-with search
    # '=' Exact matches
    # '@' Full-text search (Currently only supported Django's MySQL backend.)
    # '$' Regex search
    search_fields = ('^username', '^full_name',)
    # ordering_fields = ('',)

    def get_queryset(self):
        queryset = MyUser.objects.all()
        username = self.request.query_params.get('username', None)
        full_name = self.request.query_params.get('full_name', None)

        if username and full_name is not None:
            queryset = queryset.filter(username=username, full_name=full_name)
        elif username is not None:
            queryset = queryset.filter(username=username)
        elif full_name is not None:
            queryset = queryset.filter(full_name=full_name)
        return queryset
