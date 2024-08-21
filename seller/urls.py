# sellers/urls.py
from django.urls import path
from .views import SellerProductView

urlpatterns = [
    path('products/', SellerProductView.as_view()),  # For sellers to view/add products
    path('products/<int:pk>/', SellerProductView.as_view()),  # For sellers to update/delete products
]
