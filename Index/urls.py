from django.conf.urls import url
from Index import views

urlpatterns = [
    url('^$', views.index)
]