from django.conf.urls import url
from Pay import views


urlpatterns = [
    url(r'pay_yl/', views.pay_yl),
    url(r'pay_wx/', views.pay_wx),
    url(r'pay_ali/', views.pay_ali),
    url(r'update_order/', views.pay_yl),
    url(r'', views.pay),

]