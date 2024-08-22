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

        # Start with a base queryset (all products)
        queryset = Product.objects.all()

        # Apply filtering based on category
        if category:
            queryset = queryset.filter(category__category_name=category)

        # Apply filtering based on search term
        if search:
            queryset = queryset.filter(product_name__icontains=search)  # Use icontains for case-insensitive search

        # Serialize the (filtered) queryset
        serializer = ProductSerializer(queryset, many=True)

        # Return all products if no filters are applied or after applying filters
        return Response({'count': len(serializer.data), 'data': serializer.data})


class DemoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        return Response({'success': 'Hurray you are authenticated!'})
