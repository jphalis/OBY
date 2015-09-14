from django.conf.urls import patterns, url

from .views import (AccountCreateAPIView, FollowerListAPIView, HomepageAPIView,
                    MyUserDetailAPIView, MyUserListAPIView)
from .views import (CommentCreateAPIView, CommentDetailAPIView,
                    CommentListAPIView)
from .views import DonationListAPIView
from .views import HashtagListAPIView
from .views import (CategoryDetailAPIView, CategoryListAPIView,
                    PhotoListAPIView, PhotoCreateAPIView, PhotoDetailAPIView,
                    TimelineAPIView)
from .views import NotificationAPIView


urlpatterns = patterns('',
    url(r'^$', 'api.views.api_home',
        name='api_home'),
    url(r'^account/create/$', AccountCreateAPIView.as_view(),
        name='account_create_api'),
    url(r'^categories/$', CategoryListAPIView.as_view(),
        name='category_list_api'),
    url(r'^categories/(?P<slug>[\w-]+)/$', CategoryDetailAPIView.as_view(),
        name='category_detail_api'),
    url(r'^comments/$', CommentListAPIView.as_view(),
        name='comment_list_api'),
    url(r'^comment/create/$', CommentCreateAPIView.as_view(),
        name='comment_create_api'),
    url(r'^comment/(?P<id>\d+)/$', CommentDetailAPIView.as_view(),
        name='comment_detail_api'),
    url(r'^donations/$', DonationListAPIView.as_view(),
        name='donation_list_api'),
    url(r'^follows/$', FollowerListAPIView.as_view(),
        name='follow_list_api'),
    url(r'^hashtags/$', HashtagListAPIView.as_view(),
        name='hashtag_list_api'),
    url(r'^homepage/$', HomepageAPIView.as_view(),
        name='homepage_api'),
    url(r'^notifications/$', NotificationAPIView.as_view(),
        name='notification_list_api'),
    url(r'^photos/$', PhotoListAPIView.as_view(),
        name='photo_list_api'),
    url(r'^photo/create/$', PhotoCreateAPIView.as_view({'post': 'create'}),
        name='photo_create_api'),
    url(r'^photo/(?P<cat_slug>[\w-]+)/(?P<photo_slug>[\w-]+)/$',
        PhotoDetailAPIView.as_view(), name='photo_detail_api'),
    url(r'^profiles/$', MyUserListAPIView.as_view(),
        name='user_profile_list_api'),
    url(r'^profiles/(?P<username>[\w.@+-]+)/$', MyUserDetailAPIView.as_view(),
        name='user_profile_detail_api'),
    url(r'^timeline/$', TimelineAPIView.as_view(),
        name='timeline_api'),
)
