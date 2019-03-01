from django.conf.urls import url
from Login import views

urlpattenrns = [
    url(r'^$', views.login)
]