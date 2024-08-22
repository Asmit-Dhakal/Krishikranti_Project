# utils.py

from django.utils.crypto import get_random_string
from .models import Order, OrderItem

def generate_unique_order_id():
    return get_random_string(length=12, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def create_order_from_cart(cart, user):
    # Create the Order instance
    order = Order.objects.create(
        user=user,
        cart=cart,
        order_id=generate_unique_order_id(),
        amount=sum(item.price for item in cart.items.all())
    )

    # Create OrderItem instances
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.price
        )

    return order
