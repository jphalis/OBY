from django.conf.urls import patterns, url


urlpatterns = patterns('newsletter.views',
    url(r'^toggle_newsletter/$', 'toggle_newsletter',
        name='toggle_newsletter'),
)
