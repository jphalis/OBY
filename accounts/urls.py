from django.conf.urls import patterns, url


urlpatterns = patterns('accounts.views',
    url(r'^account/$', 'account_settings', name='account_settings'),
    url(r'^signout/$', 'auth_logout', name='logout'),
    url(r'^password/change/$', 'password_change', name="password_change"),
    url(r'^password/reset/$', 'password_reset', name="password_reset"),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm',
        name="password_reset_confirm"),
)
