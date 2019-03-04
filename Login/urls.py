from django.conf.urls import url
from Login import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^register/$', views.register),
    url(r'^register_exit/$', views.register_exit),

]