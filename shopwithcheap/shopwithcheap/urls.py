# from django.contrib import admin
from django.urls import path, include # type: ignore
from client_panel import views

# from client_panel import views as client_panel_views

urlpatterns = [
    path('', include('client_panel.urls')),  # This sets the root URL to client_panel
    path('admin/', include('admin_panel.urls')),
]
