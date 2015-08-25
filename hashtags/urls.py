from django.conf.urls import patterns, url


urlpatterns = patterns('hashtags.views',
    url(r'^(?P<tag>[\w-]+)/$', 'hashtagged_item_list',
        name='hashtagged_item_list'),
)
