from django.db import models

# Create your models here.
from django.db import models
from seller.models import Seller
# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='shop/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=True, null=True )

    def __str__(self):
        return self.product_name




