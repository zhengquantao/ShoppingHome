from django.conf.urls import url
from ShoppingCar import views

urlpatterns = [
    url(r'$', views.shoppingCar)
]