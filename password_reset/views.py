from django.shortcuts import render

# Create your views here.
# password_reset/views.py

import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.conf import settings
from .models import PasswordResetOTP
from .serializers import SetNewPasswordSerializer

class RequestOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            expiration_time = timezone.now() + timezone.timedelta(minutes=10)
            PasswordResetOTP.objects.update_or_create(
                user=user,
                defaults={'otp': otp, 'expires_at': expiration_time}
            )
            send_mail(
                'Your Password Reset OTP',
                f'Your OTP for password reset is {otp}. It is valid for 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordWithOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(email=email)
            otp_entry = PasswordResetOTP.objects.get(user=user, otp=otp)

            if otp_entry.expires_at < timezone.now():
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = SetNewPasswordSerializer(data={'new_password': new_password})
            if serializer.is_valid():
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                otp_entry.delete()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or OTP'}, status=status.HTTP_404_NOT_FOUND)
        except PasswordResetOTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
