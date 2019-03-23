from django.conf.urls import url
from ShoppingCar import views

urlpatterns = [
    url(r'^$', views.shopping_car),
    url(r'^carShow/$', views.car_show),
    url(r'^car_update/', views.car_update),
]