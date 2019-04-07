from django.conf.urls import url
from Detail import views

urlpatterns = [
    url(r'^comment/', views.comment),
    url(r'^Ccomment/', views.child_comment),
    url(r'', views.detail),

]