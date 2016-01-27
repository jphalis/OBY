# from collections import Counter
# from itertools import chain

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import get_object_or_404, Http404
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from rest_framework import generics, mixins, permissions, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import Follower, MyUser
from comments.models import Comment
from core.mixins import AdminRequiredMixin, CacheMixin
from flag.models import Flag
from hashtags.models import Hashtag
from notifications.models import Notification
from notifications.signals import notify
from photos.models import Category, Photo
from push_notifications.models import APNSDevice
from shop.models import Product
from shop.signals import listuse_status_check
from .account_serializers import (AccountCreateSerializer, FollowerSerializer,
                                  MyUserSerializer)
from .auth_serializers import (PasswordResetSerializer,
                               PasswordResetConfirmSerializer,
                               PasswordChangeSerializer)
from .comment_serializers import (CommentCreateSerializer,
                                  CommentUpdateSerializer)
from .hashtag_serializers import HashtagSerializer
from .mixins import DefaultsMixin, FiltersMixin
from .notification_serializers import NotificationSerializer
from .pagination import (AccountPagination, HashtagPagination,
                         NotificationPagination, PhotoPagination,
                         ShopPagination)
from .permissions import (IsAdvertiser, IsCreatorOrReadOnly, IsOwnerOrReadOnly,
                          MyUserIsOwnerOrReadOnly)
from .photo_serializers import (CategorySerializer, PhotoCreateSerializer,
                                PhotoSerializer)
from .search_serializers import SearchMyUserSerializer
from .shop_serializers import ProductCreateSerializer, ProductSerializer

# Create your views here.


class APIHomeView(AdminRequiredMixin, CacheMixin, DefaultsMixin, APIView):
    cache_timeout = 60 * 60 * 24 * 30

    def get(self, request, format=None):
        data = {
            'authentication': {
                'apns': api_reverse('create_apns_device', request=request),
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
                'url': api_reverse('category_list_api', request=request),
            },
            'comments': {
                'create_url': api_reverse('comment_create_api',
                                          request=request),
            },
            'hashtags': {
                'display_photos': api_reverse('hashtag_photo_list_api',
                                              request=request),
                # 'trending_tags': api_reverse('hashtag_trending_list_api',
                #                              request=request),
            },
            'homepage': {
                'url': api_reverse('homepage_api', request=request),
            },
            'notifications': {
                'url': api_reverse('notification_list_api', request=request),
                'unread_url': api_reverse('get_unread_notifications_api',
                                          request=request),
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
            # 'shop': {
            #     'count': Product.objects.all().count(),
            #     'url': api_reverse('product_list_api', request=request),
            #     'create_url': api_reverse('product_create_api',
            #                               request=request),
            # },
            'timeline': {
                'url': api_reverse('timeline_api', request=request),
            },
        }
        return RestResponse(data)


class HomepageAPIView(CacheMixin, DefaultsMixin, generics.ListAPIView):
    cache_timeout = 60 * 7
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.most_liked_offset()[:30]


class TimelineAPIView(CacheMixin, DefaultsMixin, generics.ListAPIView):
    cache_timeout = 60 * 7
    serializer_class = PhotoSerializer

    def get_queryset(self):
        user = self.request.user
        photos_self = Photo.objects.own(user)

        try:
            follow = Follower.objects.select_related('user').get(user=user)
        except Follower.DoesNotExist:
            follow = None

        if follow:
            if follow.following.count() == 0:
                photos_suggested = Photo.objects.suggested(user)[:50]
                return photos_suggested
            else:
                photos_following = Photo.objects.following(user)
                return (photos_self | photos_following).distinct()[:250]
        else:
            # Add suggested users
            photos_suggested = Photo.objects.suggested(user)[:50]
            return photos_suggested


# A C C O U N T S
@api_view(['POST'])
def follow_create_api(request, user_pk):
    viewing_user = request.user
    follower, created = Follower.objects.get_or_create(user=viewing_user)
    user = get_object_or_404(MyUser, pk=user_pk)
    followed, created = Follower.objects.get_or_create(user=user)

    try:
        user_followed = (Follower.objects.select_related('user')
                                         .get(user=user, followers=follower))
    except Follower.DoesNotExist:
        user_followed = None

    if user_followed:
        followed.followers.remove(follower)
        viewing_user.available_points = F('available_points') - 1
        viewing_user.total_points = F('total_points') - 1
    else:
        followed.followers.add(follower)
        viewing_user.available_points = F('available_points') + 1
        viewing_user.total_points = F('total_points') + 1
        notify.send(
            request.user,
            recipient=user,
            verb='is now supporting you'
        )

        # Push notifications
        try:
            device = APNSDevice.objects.get(user=user)
        except APNSDevice.DoesNotExist:
            device = None

        if device:
            # Alert message may only be sent as text.
            device.send_message(
                "{} is now supporting you.".format(viewing_user))
            # No alerts but with badge.
            # device.send_message(None, badge=1)
            # Silent message with badge and added custom data.
            # device.send_message(None, badge=1, extra={"foo": "bar"})

        if user in viewing_user.blocking.all():
            viewing_user.blocking.remove(user)
    serializer = FollowerSerializer(followed, context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def block_user_api(request, user_pk):
    viewing_user = request.user
    user_to_block = get_object_or_404(MyUser, pk=user_pk)
    follower, created = Follower.objects.get_or_create(user=viewing_user)
    followed, created = Follower.objects.get_or_create(user=user_to_block)

    # Does the viewing_user follow the user_to_block?
    # If so, remove them
    try:
        user_to_block_followed = (Follower.objects.select_related('user')
                                          .get(user=user_to_block,
                                               followers=follower))
    except Follower.DoesNotExist:
        user_to_block_followed = None

    if user_to_block_followed:
        followed.followers.remove(follower)

    # Does the user_to_block follow the viewing_user?
    # If so, remove them
    try:
        viewer_followed = (Follower.objects.select_related('user')
                                           .get(user=viewing_user,
                                                followers=followed))
    except Follower.DoesNotExist:
        viewer_followed = None

    if viewer_followed:
        follower.followers.remove(followed)

    # Is the user_to_block already in blocked users?
    if user_to_block not in viewing_user.blocking.all():
        viewing_user.blocking.add(user_to_block)

    serializer = FollowerSerializer(followed, context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


class AccountCreateAPIView(generics.CreateAPIView):
    serializer_class = AccountCreateSerializer
    permission_classes = (permissions.AllowAny,)


class MyUserListAPIView(CacheMixin, DefaultsMixin, generics.ListAPIView):
    cache_timeout = 60 * 60 * 24
    pagination_class = AccountPagination
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()


class MyUserDetailAPIView(CacheMixin,
                          generics.RetrieveAPIView,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin):
    cache_timeout = 60 * 5
    permission_classes = (
        permissions.IsAuthenticated,
        MyUserIsOwnerOrReadOnly,
    )
    serializer_class = MyUserSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        username = self.kwargs["username"]
        obj = get_object_or_404(MyUser, username=username)
        if self.request.user in obj.blocking.all():
            raise PermissionDenied(
                "You do not have permission to view that profile.")
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
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return RestResponse({"success": "Password has been reset."})


class PasswordChangeView(generics.GenericAPIView):
    """
    Calls SetPasswordForm save method
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return RestResponse({"success": "New password has been saved."})


# C O M M E N T S
class CommentCreateAPIView(CacheMixin, generics.CreateAPIView):
    serializer_class = CommentCreateSerializer

    def post(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        parent_id = self.request.data.get('parent')
        photo_id = self.request.data.get('photo')
        parent_comment = None
        photo = (Photo.objects.select_related('category', 'creator')
                              .get(id=photo_id))
        photo_creator = photo.creator

        if parent_id is not None:
            try:
                parent_comment = Comment.objects.select_related(
                    'user', 'photo').get(id=parent_id)
            except:
                parent_comment = None
            if parent_comment is not None and parent_comment.photo is not None:
                photo = parent_comment.photo

        if serializer.is_valid():
            comment_text = self.request.data.get('text')
            if parent_comment is not None:
                # parent comments exists
                new_child_comment = Comment.objects.create_comment(
                    user=user,
                    path=parent_comment.get_origin,
                    text=comment_text,
                    photo=photo,
                    parent=parent_comment
                )
                affected_users = parent_comment.get_affected_users()
                notify.send(
                    user,
                    action=new_child_comment,
                    target=parent_comment,
                    recipient=parent_comment.user,
                    affected_users=affected_users,
                    verb='replied to'
                )
            else:
                new_parent_comment = Comment.objects.create_comment(
                    user=user,
                    path=request.get_full_path,
                    text=comment_text,
                    photo=photo
                )
                notify.send(
                    user,
                    action=new_parent_comment,
                    target=new_parent_comment.photo,
                    recipient=photo_creator,
                    verb='commented'
                )

                # Push notifications
                if user != photo_creator:
                    try:
                        device = APNSDevice.objects.get(user=photo_creator)
                    except APNSDevice.DoesNotExist:
                        device = None

                    if device:
                        # Alert message may only be sent as text.
                        device.send_message(
                            "{} commented on your photo.".format(user))
                        # No alerts but with badge.
                        # device.send_message(None, badge=1)
                        # Silent message with badge and added custom data.
                        # device.send_message(None, badge=1, extra={"foo": "bar"})
            if user != photo_creator:
                user.available_points = F('available_points') + 1
                user.total_points = F('total_points') + 1
                user.save()
            return RestResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        else:
            return RestResponse(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(CacheMixin,
                           generics.RetrieveAPIView,
                           mixins.DestroyModelMixin):
    cache_timeout = 60 * 7
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = CommentUpdateSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = (Comment.objects.select_related('user', 'photo')
                                   .filter(pk__gte=0))
        return queryset

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# F L A G S
@api_view(['POST'])
def flag_create_api(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    photo_creator = photo.creator

    flagged, created = Flag.objects.get_or_create(photo=photo,
                                                  creator=request.user)
    flagged.flag_count = F('flag_count') + 1
    flagged.save()

    photo_creator.times_flagged = F('times_flagged') + 1
    photo_creator.save()

    send_mail('FLAGGED ITEM',
              'There is a new flagged item with the id: {}'.format(flagged.id),
              settings.EMAIL_FROM, ['team@obystudio.com'], fail_silently=False)

    serializer = PhotoSerializer(photo, context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


# H A S H T A G S
class HashtagTrendingListAPIView(CacheMixin, DefaultsMixin,
                                 generics.ListAPIView):
    cache_timeout = 60 * 7
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()

    # def get_queryset(self):
    #     hashtags = [u'#{}'.format(tag) for tag in Hashtag.objects.values_list(
    #         'tag', flat=True)]
    #     for description in Photo.objects.values_list('description', flat=True):
    #         description_words = description.split(' ')
    #         hashtag_counts = Counter(
    #             [word for word in description_words if word in hashtags]) \
    #             .most_common()
    #     return hashtag_counts


class HashtagPhotoListAPIView(CacheMixin, DefaultsMixin, FiltersMixin,
                              generics.ListAPIView):
    cache_timeout = 60 * 7
    serializer_class = PhotoSerializer
    pagination_class = HashtagPagination

    def get_queryset(self):
        queryset = (Photo.objects.select_related('creator', 'category')
                                 .prefetch_related('likers'))
        tag = self.request.query_params.get('q', None)

        if tag is not None:
            queryset = queryset.filter(
                description__icontains='#{}'.format(tag))
        return queryset


# N O T I F I C A T I O N S
class NotificationAPIView(CacheMixin, DefaultsMixin, generics.ListAPIView):
    cache_timeout = 60 * 7
    pagination_class = NotificationPagination
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        # Show 50, but delete all objects after the 50
        notifications = Notification.objects.all_for_user(user)
        for notification in notifications:
            if notification.recipient == user:
                notification.read = True
                notification.save()
            else:
                raise Http404
        return notifications


class NotificationAjaxAPIView(CacheMixin, DefaultsMixin, generics.ListAPIView):
    pagination_class = NotificationPagination
    serializer_class = NotificationSerializer

    def get_queryset(self):
        notifications = Notification.objects.all_unread(
            self.request.user)[:1]
        return notifications


# P H O T O S
@api_view(['POST'])
def like_create_api(request, photo_pk):
    user = request.user
    photo = get_object_or_404(Photo, pk=photo_pk)
    photo_creator = photo.creator

    if user in photo.likers.all():
        photo.likers.remove(user)
        if user != photo_creator:
            user.available_points = F('available_points') - 1
            user.total_points = F('total_points') - 1
            user.save()
    else:
        photo.likers.add(user)
        if user != photo_creator:
            user.available_points = F('available_points') + 1
            user.total_points = F('total_points') + 1
            user.save()
        notify.send(
            user,
            action=photo,
            target=photo,
            recipient=photo_creator,
            verb='liked'
        )

        # Push notifications
        if user != photo_creator:
            try:
                device = APNSDevice.objects.get(user=photo_creator)
            except APNSDevice.DoesNotExist:
                device = None

            if device:
                # Alert message may only be sent as text.
                device.send_message("{} liked your photo.".format(user))
                # No alerts but with badge.
                # device.send_message(None, badge=1)
                # Silent message with badge and added custom data.
                # device.send_message(None, badge=1, extra={"foo": "bar"})

    serializer = PhotoSerializer(photo, context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


class PhotoCreateAPIView(ModelViewSet):
    queryset = Photo.objects.select_related('creator').all()
    serializer_class = PhotoCreateSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        user = self.request.user
        user.available_points = F('available_points') + 1
        user.total_points = F('total_points') + 1
        user.save()
        serializer.save(creator=user,
                        slug=get_random_string(length=10),
                        photo=self.request.data.get('photo'))


class PhotoListAPIView(CacheMixin, DefaultsMixin, FiltersMixin,
                       generics.ListAPIView):
    cache_timeout = 60 * 60 * 24
    pagination_class = PhotoPagination
    serializer_class = PhotoSerializer
    queryset = (Photo.objects.select_related('creator', 'category')
                             .prefetch_related('likers'))
    search_fields = ('description',)
    ordering_fields = ('created', 'modified',)


class PhotoDetailAPIView(CacheMixin,
                         generics.RetrieveAPIView,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin):
    cache_timeout = 60 * 7
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrReadOnly,)
    serializer_class = PhotoSerializer

    def get_object(self):
        cat_slug = self.kwargs["cat_slug"]
        photo_slug = self.kwargs["photo_slug"]
        category = get_object_or_404(Category, slug=cat_slug)
        obj = get_object_or_404(Photo, category=category, slug=photo_slug)
        return obj

    def delete(self, request, *args, **kwargs):
        cat_slug = self.kwargs["cat_slug"]
        photo_slug = self.kwargs["photo_slug"]
        category = get_object_or_404(Category, slug=cat_slug)
        obj = get_object_or_404(Photo, category=category, slug=photo_slug)
        if request.user == obj.creator:
            return self.destroy(request, *args, **kwargs)
        raise PermissionDenied(
            {"message": "You don't have permission to access this"})

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CategoryListAPIView(CacheMixin, DefaultsMixin, generics.ListAPIView):
    cache_timeout = 60 * 7
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.most_posts()


class CategoryDetailAPIView(CacheMixin, DefaultsMixin,
                            generics.RetrieveAPIView):
    cache_timeout = 60 * 7
    serializer_class = CategorySerializer

    def get_object(self):
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Category, slug=slug)
        return obj


# S E A R C H
class SearchListAPIView(CacheMixin, DefaultsMixin, FiltersMixin,
                        generics.ListAPIView):
    serializer_class = SearchMyUserSerializer
    # '^' Starts-with search
    # '=' Exact matches
    # '$' Regex search
    search_fields = ('^username', '^full_name',)

    def get_queryset(self):
        queryset = (MyUser.objects.filter(is_active=True)
                                  .only('id', 'username', 'full_name',
                                        'profile_picture'))
        return queryset


# S H O P
@api_view(['GET'])
def reward_check_view(request):
    context = {
        'deserves_reward':
            request.user.available_points >= settings.DESERVES_REWARD_AMOUNT,
    }
    return RestResponse(context)


@api_view(['GET'])
def reward_redeemed_view(request):
    user = request.user
    user.available_points = F('available_points') - settings.DESERVES_REWARD_AMOUNT
    user.save()
    return RestResponse(status=status.HTTP_202_ACCEPTED)


# Need to fix the list_use_date_start
class ProductCreateAPIView(ModelViewSet):
    queryset = Product.objects.select_related('owner')
    serializer_class = ProductCreateSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        slug=slugify(self.request.data.get('title')),
                        image=self.request.data.get('image'))


class ProductListAPIView(CacheMixin, DefaultsMixin, FiltersMixin,
                         generics.ListAPIView):
    cache_timeout = 60 * 60 * 24
    pagination_class = ShopPagination
    serializer_class = ProductSerializer
    search_fields = ('title', 'owner',)
    ordering_fields = ('created', 'modified', 'list_date_start',)

    def get_queryset(self):
        products = (Product.objects.select_related('owner')
                                   .prefetch_related('buyers'))
        for product in products:
            listuse_status_check.send(sender=product)
        queryset = products.filter(is_listed=True)
        return queryset


class ProductDetailAPIView(CacheMixin, DefaultsMixin,
                           generics.RetrieveAPIView,
                           mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin):
    cache_timeout = 60 * 60 * 24
    permission_classes = (IsAdvertiser, IsOwnerOrReadOnly,)
    queryset = (Product.objects.select_related('owner')
                               .prefetch_related('buyers'))
    serializer_class = ProductSerializer

    def get_object(self):
        product_slug = self.kwargs["product_slug"]
        obj = get_object_or_404(Product, slug=product_slug)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
