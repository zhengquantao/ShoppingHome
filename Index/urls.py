from django.conf.urls import url
from Index import views

urlpatterns = [
    url(r'^list/', views.list),
    url(r'^', views.index),


]