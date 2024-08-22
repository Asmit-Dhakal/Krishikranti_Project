# sellers/serializers.py
from rest_framework import serializers
from .models import Seller

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'store_name']
