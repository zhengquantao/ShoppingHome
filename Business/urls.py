from django.conf.urls import url
from Business import views


urlpatterns = [
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^index/', views.index),
    url(r'^shop/', views.shop),
    url(r'^list/', views.list),
    url(r'^add/', views.add),
    url(r'^update/', views.update),
    url(r'^search/', views.search),
    url(r'^message/', views.message),
    url(r'^active/', views.active),
    url(r'^ad/', views.ad),
    # url(r'^chat/', views.chat),
]