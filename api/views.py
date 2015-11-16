from itertools import chain

from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework import filters, generics, mixins, permissions, status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Follower, MyUser
from comments.models import Comment
from hashtags.models import Hashtag
from notifications.models import Notification
from photos.models import Category, Photo
from .account_serializers import AccountCreateSerializer, MyUserSerializer
from .auth_serializers import (PasswordResetSerializer,
                               PasswordResetConfirmSerializer,
                               PasswordChangeSerializer)
from .comment_serializers import (CommentCreateSerializer, CommentSerializer,
                                  CommentUpdateSerializer)
from .hashtag_serializers import HashtagSerializer
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


class APIHomeView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        data = {
            'authentication': {
                'login': api_reverse('auth_login_api', request=request),
                'password_reset': api_reverse('rest_password_reset',
                                              request=request),
                'password_change': api_reverse('rest_password_change',
                                               request=request)
            },
            'accounts': {
                'count': MyUser.objects.all().count(),
                'url': api_reverse('user_account_list_api', request=request),
                'create_url': api_reverse('account_create_api',
                                          request=request),
                'edit_profile_url': api_reverse(
                    'user_account_detail_api', request=request,
                    kwargs={'username': request.user.username})
            },
            'categories': {
                # 'count': Category.objects.all().count(),
                'url': api_reverse('category_list_api', request=request),
            },
            'comments': {
                'count': Comment.objects.all().count(),
                'url': api_reverse('comment_list_api', request=request),
                'create_url': api_reverse('comment_create_api',
                                          request=request),
            },
            # 'donations': {
            #     'count': Donation.objects.all().count(),
            #     'url': api_reverse('donation_list_api', request=request),
            # },
            'hashtags': {
                'count': Hashtag.objects.all().count(),
                'url': api_reverse('hashtag_list_api', request=request),
            },
            'homepage': {
                'url': api_reverse('homepage_api', request=request),
            },
            'notifications': {
                'url': api_reverse('notification_list_api', request=request),
            },
            'photos': {
                'count': Photo.objects.all().count(),
                'url': api_reverse('photo_list_api', request=request),
                'create_url': api_reverse('photo_create_api', request=request),
            },
            'search': {
                'url': api_reverse('search_api', request=request),
                'help_text': "add '?q=searched_parameter' to the "
                             "end of the url to display results"
            },
            'timeline': {
                'url': api_reverse('timeline_api', request=request),
            },
        }
        return RestResponse(data)


class HomepageAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.most_liked_offset()[:30]


class TimelineAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
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
class AccountCreateAPIView(generics.CreateAPIView):
    serializer_class = AccountCreateSerializer


class MyUserListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    pagination_class = AccountPagination
    permission_classes = [permissions.IsAuthenticated]
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


# class FollowerListAPIView(generics.ListAPIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication,
#                               JSONWebTokenAuthentication]
#     pagination_class = AccountPagination
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = FollowerSerializer
#     queryset = Follower.objects.all()


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


class CommentListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    pagination_class = CommentPagination
    permission_classes = [permissions.IsAuthenticated]
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


# D O N A T I O N S
# class DonationListAPIView(generics.ListAPIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication,
#                               JSONWebTokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = DonationSerializer
#     queryset = Donation.objects.all()


# H A S H T A G S
class HashtagListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    pagination_class = HashtagPagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["tag"]


# N O T I F I C A T I O N S
class NotificationAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    pagination_class = NotificationPagination
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.all_for_user(self.request.user)[:50]


# P H O T O S
class PhotoCreateAPIView(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoCreateSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user,
                        slug=get_random_string(length=10),
                        photo=self.request.data.get('photo'))


class PhotoListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    pagination_class = PhotoPagination
    permission_classes = [permissions.IsAuthenticated]
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


class CategoryListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.most_posts()


class CategoryDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Category, slug=slug)
        return obj


# S E A R C H
class SearchListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SearchMyUserSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend,)
    # '^' Starts-with search
    # '=' Exact matches
    # '@' Full-text search (Currently only supported Django's MySQL backend.)
    # '$' Regex search
    search_fields = ['^username', '^full_name']

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
