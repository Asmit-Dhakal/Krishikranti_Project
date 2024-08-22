from django.urls import path
from .views import SellerProductView

urlpatterns = [
    path('products/', SellerProductView.as_view(), name='product-list'),  # For GET (list) and POST
    path('products/<int:pk>/', SellerProductView.as_view(), name='product-detail'),  # For GET, PATCH, DELETE
]
