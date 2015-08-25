from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Follower, MyUser
from comments.models import Comment
from hashtags.models import Hashtag
from notifications.models import Notification
from photos.models import Category, Photo

from rest_framework.decorators import api_view
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse

from .account_serializers import (AccountCreateSerializer, FollowerSerializer,
                                  MyUserSerializer)
from .comment_serializers import (CommentCreateSerializer, CommentSerializer,
                                  CommentUpdateSerializer)
from .hashtag_serializers import HashtagSerializer
from .notification_serializers import NotificationSerializer
from .permissions import (IsCreatorOrReadOnly, IsOwnerOrReadOnly,
                          MyUserIsOwnerOrReadOnly)
from .photo_serializers import (CategorySerializer, PhotoCreateSerializer,
                                PhotoSerializer)

# Create your views here.


@api_view(['GET'])
def api_home(request):
    data = {
        'profiles': {
            'count': MyUser.objects.all().count(),
            'url': api_reverse('user_profile_list_api'),
        },
        'categories': {
            'count': Category.objects.all().count(),
            'url': api_reverse('category_list_api'),
        },
        'comments': {
            'count': Comment.objects.all().count(),
            'url': api_reverse('comment_list_api'),
        },
        'hashtags': {
            'count': Hashtag.objects.all().count(),
            'url': api_reverse('hashtag_list_api'),
        },
        'homepage': {
            'url': api_reverse('homepage_api'),
        },
        'notifications': {
            'url': api_reverse('notification_list_api'),
        },
        'photos': {
            'count': Photo.objects.all().count(),
            'url': api_reverse('photo_list_api'),
        },
        'timeline': {
            'url': api_reverse('timeline_api'),
        },
    }
    return RestResponse(data)


# A C C O U N T S
class AccountCreateAPIView(generics.CreateAPIView):
    serializer_class = AccountCreateSerializer


class MyUserListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    paginate_by = 250


class MyUserDetailAPIView(generics.RetrieveAPIView,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin):
    permission_classes = [MyUserIsOwnerOrReadOnly]
    serializer_class = MyUserSerializer

    def get_object(self):
        username = self.kwargs["username"]
        obj = get_object_or_404(MyUser, username=username)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class FollowerListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()


class HomepageAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.most_liked_offset()[:8]


# C O M M E N T S
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer


class CommentListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    paginate_by = 150


class CommentDetailAPIView(mixins.DestroyModelMixin, generics.RetrieveAPIView):
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]
    serializer_class = CommentUpdateSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.filter(pk__gte=0)
        return queryset

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# H A S H T A G S
class HashtagListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()
    paginate_by = 250


# N O T I F I C A T I O N S
class NotificationAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()


# P H O T O S
class PhotoCreateAPIView(generics.CreateAPIView):
    serializer_class = PhotoCreateSerializer


class PhotoListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    paginate_by = 250


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
        return Category.objects.annotate(
            the_count=(Count('photo'))).filter(
                is_active=True).order_by('-the_count')


class CategoryDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Category, slug=slug)
        return obj


class TimelineAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer

    def get_queryset(self):
        photos_self = Photo.objects.own(self.request.user)
        photos_following = Photo.objects.following(self.request.user)
        return (photos_self | photos_following).distinct()
