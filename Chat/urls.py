from django.conf.urls import url
from Chat import views

urlpatterns = [
    url(r'^update', views.update),
    url(r'^change/', views.change),
    # url(r'^websocket/', views.web_socket),
    url(r'^$', views.chat),
]