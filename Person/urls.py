from django.conf.urls import url
from Person import views

urlpatterns = [
    url(r'^$', views.person),
    url(r'^address/$', views.address),
    url(r'^order/', views.order),
    url(r'^update/$', views.address_update),
    url(r'^coupon/$', views.coupon),
]