"""ShoppingHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from Index import urls as index
from Login import urls as login
from Person import urls as person
from Detail import urls as detail
from ShoppingCar import urls as shopping_car
from Business import urls as business
from Express import urls as express
from Pay import urls as pay
from Chat import urls as chat
from Seckill import urls as seckill
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pay/', include(pay)),
    url(r'^detail/', include(detail)),
    url(r'^login/', include(login)),
    url(r'^person/', include(person)),
    url(r'^shoppingCar/', include(shopping_car)),
    url(r'^business/', include(business)),
    url(r'^express/', include(express)),
    url(r'^chat/', include(chat)),
    url(r'^seckill/', include(seckill)),
    url(r'^', include(index)),

]
