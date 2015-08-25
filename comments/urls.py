from django.conf.urls import patterns, url


urlpatterns = patterns('comments.views',
    url(r'^create/$', 'comment_create_view',
        name='comment_create'),
    url(r'^(?P<cat_slug>[\w-]+)/(?P<photo_slug>[\w-]+)/comments/$',
        'comments_all',
        name='comments_all'),
    url(r'^(?P<id>\d+)/$', 'comment_thread',
        name='comment_thread'),
)
