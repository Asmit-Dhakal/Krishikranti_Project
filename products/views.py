from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer

class ProductView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        search = request.query_params.get('search')

        # Start with a base queryset
        queryset = Product.objects.all()

        # Filter by category if provided
        if category:
            queryset = queryset.filter(category__category_name=category)

        # Filter by search term if provided
        if search:
            queryset = queryset.filter(product_name__icontains=search)  # Use icontains for case-insensitive search

        # Serialize the filtered queryset
        serializer = ProductSerializer(queryset, many=True)

        # Check if no products are found
        if not serializer.data:
            return Response({'message': 'No products found'}, status=404)  # HTTP 404 Not Found

        return Response({'count': len(serializer.data), 'data': serializer.data})


class DemoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        return Response({'success': 'Hurray you are authenticated!'})
