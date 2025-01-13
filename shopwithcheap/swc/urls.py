from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Client-side views
    path('', views.INDEX, name="home"),  # Home page for clients

    # Admin panel views
    path('admin-custom/', views.ADMININDEX, name="custom_admin"),  # Custom admin page
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
