from django.conf.urls import url
from Person import views

urlpattenrns = [
    url(r'^$', views.person)
]