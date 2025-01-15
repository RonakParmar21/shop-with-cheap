from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Client-side views
    # path('', views.INDEX, name="home"),  
    path('', views.home_view, name="home"),
    path('signup/', views.register_user, name='signup'),
    path('login/', views.login_user, name='login'), 
    path('prodgrid/', views.prod_grid, name='prodgrid'),
    path('logout/', views.logout_user, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search-products/', views.searched_products, name='search_products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),

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
