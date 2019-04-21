from django.conf.urls import url
from Seckill import views

urlpatterns = [
    url(r'^inseckill/', views.inRedis),
    url(r'^sendkill/', views.sendKill),
    url(r'^goodkill/', views.goodkill),
    url(r'$', views.seckill),

]