from django.conf.urls import patterns, url

from .views import PhotoDelete


urlpatterns = patterns('photos.views',
    url(r'^categories/(?P<cat_slug>[\w-]+)/$', 'category_detail',
        name='category_detail'),
    url(r'^delete/(?P<pk>\d+)/$', PhotoDelete.as_view(),
        name="delete_photo"),
    url(r'^like/$', 'like_ajax', name='like_ajax'),
    url(r'^upload/$', 'photo_upload', name='photo_upload'),
)
