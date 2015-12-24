from django.conf.urls import url

from . import views
from .views import APIHomeView, HomepageAPIView, TimelineAPIView
from .views import (AccountCreateAPIView,
                    MyUserDetailAPIView, MyUserListAPIView)
from .views import CommentCreateAPIView, CommentDetailAPIView
from .views import HashtagListAPIView
from .views import (CategoryDetailAPIView, CategoryListAPIView,
                    PhotoListAPIView, PhotoCreateAPIView, PhotoDetailAPIView)
from .views import NotificationAPIView, NotificationAjaxAPIView
from .views import (PasswordChangeView, PasswordResetView,
                    PasswordResetConfirmView)
from .views import ProductCreateAPIView, ProductListAPIView
from .views import SearchListAPIView


# app_name = 'api'
urlpatterns = [
    # G E N E R A L
    url(r'^$', APIHomeView.as_view(),
        name='api_home'),
    url(r'^homepage/$', HomepageAPIView.as_view(),
        name='homepage_api'),
    url(r'^timeline/$', TimelineAPIView.as_view(),
        name='timeline_api'),
    url(r'^search/$', SearchListAPIView.as_view(),
        name='search_api'),

    # A C C O U N T S
    url(r'^accounts/create/$', AccountCreateAPIView.as_view(),
        name='account_create_api'),
    url(r'^accounts/$', MyUserListAPIView.as_view(),
        name='user_account_list_api'),
    url(r'^accounts/(?P<username>[\w.@+-]+)/$', MyUserDetailAPIView.as_view(),
        name='user_account_detail_api'),
    url(r'^support/(?P<user_pk>\d+)/$', views.follow_create_api,
        name='follow_create_api'),
    # url(r'^follows/$', FollowerListAPIView.as_view(),
    #     name='follow_list_api'),

    # A U T H E N T I C A T I O N
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^password/change/$', PasswordChangeView.as_view(),
        name='rest_password_change'),

    # C O M M E N T S
    url(r'^comments/create/$', CommentCreateAPIView.as_view(),
        name='comment_create_api'),
    url(r'^comments/(?P<id>\d+)/$', CommentDetailAPIView.as_view(),
        name='comment_detail_api'),

    # H A S H T A G S
    url(r'^hashtags/$', HashtagListAPIView.as_view(),
        name='hashtag_list_api'),

    # N O T I F I C A T I O N S
    url(r'^notifications/$', NotificationAPIView.as_view(),
        name='notification_list_api'),
    url(r'^notifications/unread/$', NotificationAjaxAPIView.as_view(),
        name='get_unread_notifications_api'),

    # P H O T O S
    url(r'^categories/$', CategoryListAPIView.as_view(),
        name='category_list_api'),
    url(r'^categories/(?P<slug>[\w-]+)/$', CategoryDetailAPIView.as_view(),
        name='category_detail_api'),
    url(r'^photos/$', PhotoListAPIView.as_view(),
        name='photo_list_api'),
    url(r'^photos/create/$', PhotoCreateAPIView.as_view({'post': 'create'}),
        name='photo_create_api'),
    url(r'^photos/(?P<cat_slug>[\w-]+)/(?P<photo_slug>[\w-]+)/$',
        PhotoDetailAPIView.as_view(), name='photo_detail_api'),
    url(r'^like/(?P<photo_pk>\d+)/$', views.like_create_api,
        name='like_create_api'),

    # S H O P
    url(r'^shop/rewards/check/$', views.reward_check_view,
        name='reward_check_view'),
    url(r'^shop/rewards/redeemed/$', views.reward_redeemed_view,
        name='reward_redeemed_view'),
    url(r'^shop/$', ProductListAPIView.as_view(),
        name='product_list_api'),
    url(r'^shop/create/$', ProductCreateAPIView.as_view({'post': 'create'}),
        name='product_create_api'),
]
