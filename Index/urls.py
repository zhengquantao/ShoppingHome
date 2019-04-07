from django.conf.urls import url
from Index import views

urlpatterns = [
    url(r'^list/', views.list),
    # url(r'^chat/', views.chat),
    url(r'^search/', views.search),
    url(r'^ticket/update/', views.ticket_update),
    url(r'^ticket/', views.ticket),
    url(r'^seckill/$', views.seckill),
    url(r'^$', views.index),


]