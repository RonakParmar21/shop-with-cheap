from django.contrib import admin
from django.urls import path
from shopapp import views
from django.conf import settings
from django.conf.urls.static import static
import os 

urlpatterns = [
    path('', views.Index, name="home"),
    path('login/', views.Login, name="login"),
    path('registration/', views.Register, name="register"),
    path('contact/', views.Contact, name="contact"),
    path('search/', views.SearchProducts, name='searchproducts'),

    path('swc/', views.AdminLogin, name="adminlogin"),
    path('swc/dashboard/', views.AdminDashboard, name="admindashboard"),
    path('swc/addcategory/', views.AddCategory, name="addcategory"),
    path('swc/addsubcategory/', views.AddSubCategory, name="addsubcategory"),
    path('swc/addproduct/', views.AddProduct, name="addproduct"),
    path('swc/viewcategory/', views.ViewCategory, name="viewcategory"),
    path('swc/viewsubcategory/', views.ViewSubCategory, name="viewsubcategory"),
    path('swc/viewproduct/', views.ViewProduct, name="viewproduct"),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('swc/contactdetails/', views.ViewContactDetails, name='contactdetails'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'shopapp/static/'))