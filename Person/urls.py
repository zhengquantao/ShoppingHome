from django.conf.urls import url
from Person import views

urlpatterns = [
    url(r'^$', views.person)
]