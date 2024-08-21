from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from products.models import Product, Seller
from products.serializers import ProductSerializer
from .serializers import SellerSerializer


class SellerProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
            return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(seller=seller)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
            return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(seller=seller)
            response_data = {
                'message': 'Product successfully added',
                'product': ProductSerializer(product).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller__user=request.user)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or not owned by this seller'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller__user=request.user)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or not owned by this seller'},
                            status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellerRegistrationView(APIView):
    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            seller = Seller.objects.get(user=request.user)
            serializer = SellerSerializer(seller)
            return Response(serializer.data)
        except Seller.DoesNotExist:
            return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)


# Example of usage in URLs
from django.urls import path

urlpatterns = [
    path('api/seller/register/', SellerRegistrationView.as_view(), name='register-seller'),
    path('api/seller/products/', SellerProductView.as_view(), name='seller-products'),
    path('api/seller/products/<int:pk>/', SellerProductView.as_view(), name='seller-product-detail'),
]
