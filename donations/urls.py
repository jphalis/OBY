from django.conf.urls import patterns, url


urlpatterns = patterns('donations.views',
    url(r'^info/$', 'info', name='info'),
    url(r'^make/$', 'make', name='make'),
)
