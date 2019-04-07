from django.conf.urls import url
from Login import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^check_img/$', views.check_img),
    url(r'^email/', views.email),
    url(r'^logout/', views.logout),
    url(r'^register/$', views.register),
    url(r'^register_exit/$', views.register_exit),

]