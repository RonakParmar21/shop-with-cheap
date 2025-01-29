from django.urls import path # type: ignore
from django.conf import settings #type: ignore
from swc import views
import os
from django.conf.urls.static import static #type: ignore

urlpatterns = [
    path('', views.Index, name="home"),
    path('search/', views.SearchProducts, name='searchproducts'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('contact/', views.Contact, name="contact"),
    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('registration/', views.Register, name="register"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('get-subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
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
    path('swc/delete-contact/<int:id>/', views.DeleteContact, name='delete_contact'),
    path('swc/delete-category/<int:id>/', views.DeleteCategory, name="deletecategory"),
    path('swc/delete-subcategory/<int:id>/', views.DeleteSubCategory, name="deletesubcategory"),
    path('swc/delete-product/<int:id>/', views.DeleteProduct, name="deleteproduct"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'swc/static/'))