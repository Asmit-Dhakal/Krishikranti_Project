from django.shortcuts import render
from  rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from products.models import Product
from .serializers import *


# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=request.user
        cart =Cart.objects.filter(user=user,ordered=False).first()
        queryset =CartItem.objects.filter(cart=cart)
        serializer=CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user=request.user
        cart,_=Cart.objects.get_or_create(user=user,ordered=False)
        product =Product.objects.get(product_id =data.get("product"))
        price=Product.product_price
        quantity=data.get("quantity")
        cart_item =CartItem(cart=cart,user=user,product=product,price=price,quantity=quantity)
        cart_item.save()
        return Response({'success':'Items added to your cart'})

    def put(self, request):
        data = request.data
        cart_item_id = data.get("id")
        quantity = data.get("quantity")
        # Retrieve the CartItem instance; this will return a single object instead of a QuerySet
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'CartItem not found'}, status=404)
        # Update the quantity and save the changes
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Items updated in your cart'})

    def delete(self, request):
        user = request.user
        data =request.data
        cart_item = CartItem.objects.get(id=data.get('id'))
        cart_item.delete()
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)



class DemoView(APIView):
    def get(self, request):
        pass