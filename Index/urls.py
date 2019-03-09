from django.conf.urls import url
from Index import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/', views.list),

]