from django.conf.urls import url

from . import views


app_name = 'newsletter'
urlpatterns = [
    url(r'^toggle_newsletter/$', views.toggle_newsletter,
        name='toggle_newsletter'),
]
