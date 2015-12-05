from django.conf.urls import url

from . import views


app_name = 'notifications'
urlpatterns = [
    url(r'^$', views.all,
        name='notifications_all'),
    url(r'^ajax/$', views.get_notifications_ajax,
        name='get_notifications_ajax'),
]
