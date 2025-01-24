from django.contrib import admin
from django.urls import path
from shopapp import views

urlpatterns = [
    path('', views.Index, name="home"),
    path('login/', views.Login, name="login"),
    path('registration/', views.Register, name="register"),

    path('swc/', views.AdminLogin, name="adminlogin"),
    path('swc/dashboard/', views.AdminDashboard, name="admindashboard"),
    path('swc/addcategory', views.AddCategory, name="addcategory"),

]
