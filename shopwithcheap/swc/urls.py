from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Client-side views
    path('', views.INDEX, name="home"),  # Home page for clients

    # Admin panel views
    path('admin-custom/', views.ADMININDEX, name="custom_admin"), 
    path('admin-custom/admin-login/', views.ADMINLOGIN, name="admin_login"),
    path('admin-custom/admin-logout/', views.ADMINLOGOUT, name="admin_logout"),
    path('admin-custom/admin-showproduct/', views.SHOWPRODUCT, name="admin_showproduct"),
    path('admin-custom/admin-addsubcategory/', views.ADDSUBCATEGORY, name="admin_addsubcategory"),
    path('admin-custom/admin-showsubcategory/', views.SHOWSUBCATEGORY, name="admin_showsubcategory"),
    path('admin-custom/admin-addproduct/', views.ADDPRODUCT, name="admin_addproduct"),
    path('admin-custom/delete_subcategory/<int:subcategory_id>/', views.DELETESUBCATEGORY, name='delete_subcategory'),
    path('admin-custom/edit_subcategory/<int:subcategory_id>/', views.EDITSUBCATEGORY, name='edit_subcategory'),
    path('admin-custom/edit_product/<int:product_id>/', views.EDITPRODUCT, name='edit_product'),
    path('admin-custom/delete_product/<int:product_id>/', views.DELETEPRODUCT, name='delete_product'),
    path('get-subcategories/', views.GET_SUBCATEGORIES, name='get_subcategories'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
