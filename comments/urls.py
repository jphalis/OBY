from django.conf.urls import url

from . import views


app_name = 'comments'
urlpatterns = [
    url(r'^create/$',
        views.comment_create_view,
        name='comment_create'),
    url(r'^(?P<cat_slug>[\w-]+)/(?P<photo_slug>[\w-]+)/comments/$',
        views.comments_all,
        name='comments_all'),
    url(r'^(?P<id>\d+)/$',
        views.comment_thread,
        name='comment_thread'),
]
