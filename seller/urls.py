# sellers/urls.py
from django.urls import path
from .views import SellerProductView, SellerRegistrationView

urlpatterns = [
    path('seller/register/', SellerRegistrationView.as_view(), name='register-seller'),
    path('seller/products/', SellerProductView.as_view()),  # For sellers to view/add products
    path('seller/products/<int:pk>/', SellerProductView.as_view()),  # For sellers to update/delete products
]
