from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from products.models import Product


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    total_price=models.IntegerField(default=0)




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_item = models.IntegerField(default=0)
    price= models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name)

@receiver(post_save, sender=CartItem)
def correct_price(sender, **kwargs):
    cart_item = kwargs['instance']
    price_of_product=Product.objects.get(product_id=cart_item.product.product_id)
    total_quantity=cart_item.quantity * float(price_of_product.product_price)
    total_cart_items = CartItem.objects.filter(user=cart_item.user)
    cart_item.total_items=len(total_cart_items)