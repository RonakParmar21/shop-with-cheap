from django.urls import path
from . import views as admin_panel_views

urlpatterns = [
    path('', admin_panel_views.INDEX, name='home'),
    path('login/', admin_panel_views.LOGIN, name='login'),
    path('logout/', admin_panel_views.LOGOUT, name="logout"),
    # path('add-category/', admin_panel_views.ADDCATEGORY, name='addcategory'),
    path('add-subcategory/', admin_panel_views.ADDSUBCATEGORY, name='addsubcategory'),
    path('add-product/', admin_panel_views.ADDPRODUCT, name='addproduct'),
    # path('showcategory', admin_panel_views.SHOWCATEGORY, name="showcategory"),
    path('showsubcategory/', admin_panel_views.SHOWSUBCATEGORY, name="showsubcategory"),
    path('showproduct/', admin_panel_views.SHOWPRODUCT, name="showproduct"),

    # Add this line to handle the AJAX request for subcategories
    path('get-subcategories/', admin_panel_views.GET_SUBCATEGORIES, name='get_subcategories'),
]