from django.conf.urls import url

from . import views


app_name = 'hashtags'
urlpatterns = [
    url(r'^(?P<tag>[\w-]+)/$', views.hashtagged_item_list,
        name='hashtagged_item_list'),
]
