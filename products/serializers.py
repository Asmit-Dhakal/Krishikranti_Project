from rest_framework import serializers
from .models import Category,  Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        #fields = '__all__'
        exclude=['category_id']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested serializer to include category details
    class Meta:
        model = Product
        #fields = '__all__'
        exclude = ['product_id']


