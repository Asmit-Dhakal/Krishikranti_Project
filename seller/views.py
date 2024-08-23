from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from products.serializers import ProductSerializer

class SellerProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                product = Product.objects.get(pk=pk, seller=request.user)
                serializer = ProductSerializer(product, context={'request': request})
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found or not owned by this user'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.filter(seller=request.user)
            serializer = ProductSerializer(products, many=True, context={'request': request})
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save(seller=request.user)
            response_data = {
                'message': 'Product successfully added',
                'product': ProductSerializer(product, context={'request': request}).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or not owned by this user'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or not owned by this user'},
                            status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
