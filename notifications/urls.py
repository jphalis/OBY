from django.conf.urls import patterns, url


urlpatterns = patterns('notifications.views',
    url(r'^$', 'all', name='notifications_all'),
    url(r'^ajax/$', 'get_notifications_ajax', name='get_notifications_ajax'),
)
