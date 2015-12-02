from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin

from search.views import SearchListView


urlpatterns = patterns('',
    # ADMIN
    url(r'^hide/oby/admin/', include(admin.site.urls)),

    # GENERAL
    url(r'^about/$', 'oby.views.about', name='about'),
    url(r'^c/', include('comments.urls')),
    # url(r'^contact/', include('contact.urls')),
    url(r'^donations/', include('donations.urls', namespace='donations')),
    url(r'^hashtag/', include('hashtags.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^notifications/', include('notifications.urls')),
    url(r'^p/', include('photos.urls')),
    url(r'^privacy/$', 'oby.views.privacy_policy', name='privacy_policy'),
    url(r'^search/$', SearchListView.as_view(), name='search'),
    url(r'^ajaxsearch/$', 'search.views.search_ajax', name='search_ajax'),
    url(r'^terms/$', 'oby.views.terms_of_use', name='terms_of_use'),
    url(r'^timeline/$', 'oby.views.timeline', name='timeline'),
    url(r'^$', 'oby.views.home', name='home'),

    # API
    url(r'^hide/oby/api/', include('api.urls')),
    url(r'^hide/oby/api/auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^hide/oby/api/auth/token/$',
        'rest_framework_jwt.views.obtain_jwt_token', name='auth_login_api'),
    # url(r'^hide/oby/api/auth/token/refresh/$',
    #     'rest_framework_jwt.views.refresh_jwt_token'),
)


# ACCOUNTS
urlpatterns += patterns('accounts.views',
    url(r'^signin/$', 'auth_login', name='login'),
    url(r'^register/$', 'auth_register', name='register'),
    url(r'^follow/$', 'follow_ajax', name='follow_ajax'),
    url(r'^settings/', include('accounts.urls')),
    url(r'^supporters/(?P<username>[\w.@+-]+)/$', 'followers_thread',
        name='followers_thread'),
    url(r'^supporting/(?P<username>[\w.@+-]+)/$', 'following_thread',
        name='following_thread'),
    url(r'^(?P<username>[\w.@+-]+)/$', 'profile_view', name='profile_view'),
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    urlpatterns += patterns('',) + static(settings.STATIC_URL,
                                          document_root=settings.STATIC_ROOT)
    urlpatterns += patterns('',) + static(settings.MEDIA_URL,
                                          document_root=settings.MEDIA_ROOT)
