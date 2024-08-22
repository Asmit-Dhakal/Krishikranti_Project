from django.db import models
from django.contrib.auth.models import User

# Remove the Seller model entirely if not needed
# Just an example of what it might look like if you decide to keep it
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields if required

    def __str__(self):
        return f"Seller: {self.user.username}"
