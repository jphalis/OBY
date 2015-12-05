from django.conf.urls import url

from . import views


app_name = 'donations'
urlpatterns = [
    url(r'^info/$', views.info, name='info'),
    url(r'^make/$', views.make, name='make'),
]
