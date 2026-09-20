from django.urls import path
from . import views


urlpatterns = [
    path('', views.fee_dashboard, name='fee_dashboard'),
    path('add/', views.fee_create, name='fee_create'),
    path('<int:pk>/edit/', views.fee_update, name='fee_update'),
    path('<int:pk>/delete/', views.fee_delete, name='fee_delete'),
]