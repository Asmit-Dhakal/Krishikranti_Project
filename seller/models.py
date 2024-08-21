
from django.contrib.auth.models import User
from django.db import models

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name
