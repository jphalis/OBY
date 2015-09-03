from django.conf.urls import patterns, url


urlpatterns = patterns('donations.views',
    url(r'^completed/$', 'complete', name='complete'),
    url(r'^make/$', 'make', name='make'),
)
