from django.urls import path
from . import views

urlpatterns = [
    path('', views.INDEX, name='client_panel_index'),
]