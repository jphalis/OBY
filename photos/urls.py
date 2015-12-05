from django.conf.urls import url

from . import views
from .views import PhotoDelete


urlpatterns = [
    url(r'^categories/(?P<cat_slug>[\w-]+)/$', views.category_detail,
        name='category_detail'),
    url(r'^delete/(?P<pk>\d+)/$', PhotoDelete.as_view(),
        name="delete_photo"),
    url(r'^like/$', views.like_ajax, name='like_ajax'),
    url(r'^upload/$', views.photo_upload, name='photo_upload'),
]
