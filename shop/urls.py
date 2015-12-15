from django.conf.urls import url

from . import views


app_label = 'shop'
urlpatterns = [
    url(r'^$', views.shop,
        name='shop'),
    url(r'^create/$', views.product_create,
        name='product_create'),
    url(r'^purchase/$', views.product_purchase,
        name='product_purchase'),
]
