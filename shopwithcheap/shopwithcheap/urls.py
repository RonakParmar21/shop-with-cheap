from django.contrib import admin
from django.urls import path
from shopapp import views

urlpatterns = [
    path('', views.Index, name="home"),
    path('login/', views.Login, name="login"),

    path('swc/', views.AdminLogin, name="adminlogin"),

]
