from django.conf.urls import url

from . import views


app_name = 'contact'
urlpatterns = [
    url(r'^business/inquiry/$', views.business_inquiry,
        name='business_inquiry'),
    url(r'^business/signup/$', views.business_signup,
        name='business_signup'),
]
