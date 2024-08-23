# password_reset/urls.py

from django.urls import path
from .views import RequestOTPAPIView, ResetPasswordWithOTPAPIView

urlpatterns = [
    path('request-otp/', RequestOTPAPIView.as_view(), name='request-otp'),
    path('reset-password-otp/', ResetPasswordWithOTPAPIView.as_view(), name='reset-password-otp'),
]
