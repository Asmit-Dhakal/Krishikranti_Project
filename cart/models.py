from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.total_price}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.quantity})"

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.product_price
        super().save(*args, **kwargs)

@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    cart = instance.cart
    cart.total_price = sum(item.price for item in cart.items.all())
    cart.save()
