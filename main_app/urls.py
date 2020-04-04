from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^userlist', views.userList, name='userlist'),
]