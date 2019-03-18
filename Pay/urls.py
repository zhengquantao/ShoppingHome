from django.conf.urls import url
from Pay import views


urlpatterns = [
    url(r'', views.pay),
]