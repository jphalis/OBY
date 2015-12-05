from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from accounts import views as account_views
from rest_framework_jwt import views as rest_framework_jwt_views
from search import views as search_views
from search.views import SearchListView

from . import views


admin.site.site_header = "OBY Administration"


urlpatterns = [
    # ADMIN
    url(r'^hide/oby/admin/', include(admin.site.urls)),

    # GENERAL
    url(r'^about/$',
        views.about,
        name='about'),
    url(r'^c/', include('comments.urls',
        namespace='comments')),
    # url(r'^contact/', include('contact.urls',
    #     namespace='contact')),
    url(r'^donations/', include('donations.urls',
        namespace='donations')),
    url(r'^hashtag/', include('hashtags.urls',
        namespace='hashtags')),
    url(r'^newsletter/', include('newsletter.urls',
        namespace='newsletter')),
    url(r'^notifications/', include('notifications.urls',
        namespace='notifications')),
    url(r'^p/', include('photos.urls',
        namespace='photos')),
    url(r'^privacy/$',
        views.privacy_policy,
        name='privacy_policy'),
    url(r'^search/$',
        SearchListView.as_view(),
        name='search'),
    url(r'^ajaxsearch/$',
        search_views.search_ajax,
        name='search_ajax'),
    url(r'^terms/$',
        views.terms_of_use,
        name='terms_of_use'),
    url(r'^timeline/$',
        views.timeline,
        name='timeline'),
    url(r'^$',
        views.home,
        name='home'),

    # API
    url(r'^hide/oby/api/', include('api.urls',
        namespace='api')),
    url(r'^hide/oby/api/auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^hide/oby/api/auth/token/$',
        rest_framework_jwt_views.obtain_jwt_token,
        name='auth_login_api'),
    # url(r'^hide/oby/api/auth/token/refresh/$',
    #     'rest_framework_jwt.views.refresh_jwt_token'),
]


# ACCOUNTS
urlpatterns += [
    url(r'^signin/$',
        account_views.auth_login,
        name='login'),
    url(r'^register/$',
        account_views.auth_register,
        name='register'),
    url(r'^follow/$',
        account_views.follow_ajax,
        name='follow_ajax'),
    url(r'^settings/', include('accounts.urls',
        namespace='accounts')),
    url(r'^supporters/(?P<username>[\w.@+-]+)/$',
        account_views.followers_thread,
        name='followers_thread'),
    url(r'^supporting/(?P<username>[\w.@+-]+)/$',
        account_views.following_thread,
        name='following_thread'),
    url(r'^(?P<username>[\w.@+-]+)/$',
        account_views.profile_view,
        name='profile_view'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += [] + static(settings.STATIC_URL,
                               document_root=settings.STATIC_ROOT)
    urlpatterns += [] + static(settings.MEDIA_URL,
                               document_root=settings.MEDIA_ROOT)
