from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dash, name='dashboard'),
    path('product_management/', views.productManage, name='productManagement'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
]
