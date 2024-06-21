# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),  # Example URL pattern for home page
    path('mt5/', views.mt5_data_view, name='mt5-data'),  # Example
]