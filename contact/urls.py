from django.conf.urls import url

from . import views


app_name = 'contact'
urlpatterns = [
    url(r'^business/inquiry/$', views.business_inquiry,
        name='business_inquiry'),
]
