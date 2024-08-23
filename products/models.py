from django.db import models
from django.contrib.auth.models import User

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
    product_image = models.ImageField(upload_to='shop/images',null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Link to User

    def __str__(self):
        return self.product_name

    def image_url(self):
        if self.product_image:
            return self.product_image.url  # Directly returns the URL to the image
        return ''

    def full_image_url(self):
        if self.product_image:
            return f"http://127.0.0.1:8000{self.product_image.url}"  # Replace 127.0.0.1 with your IP if needed
        return ''
