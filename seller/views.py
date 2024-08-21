from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from products.models import Product, Seller
from products.serializers import ProductSerializer

class SellerProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller = Seller.objects.get(user=request.user)
        products = Product.objects.filter(seller=seller)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        seller = Seller.objects.get(user=request.user)
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
            return Response({'error': 'Product not found or not owned by this seller'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller__user=request.user)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or not owned by this seller'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
