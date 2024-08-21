from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s Profile"

