from django.db import models

# Create your models here.
# password_reset/models.py

from django.db import models
from django.contrib.auth.models import User

class PasswordResetOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'OTP for {self.user.email}'
