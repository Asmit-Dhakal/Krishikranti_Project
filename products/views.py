from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer

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
            queryset = queryset.filter(product_name__icontains=search)  # Case-insensitive search

        # Serialize the (filtered) queryset with request context
        serializer = ProductSerializer(queryset, many=True, context={'request': request})

        # Return all products if no filters are applied or after applying filters
        return Response({'count': len(serializer.data), 'data': serializer.data})
