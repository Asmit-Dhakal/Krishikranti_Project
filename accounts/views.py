from tokenize import TokenError

from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, ChangePasswordSerializer, UserProfileSerializer
from .models import UserProfile

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()  # Save the new user
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'address': serializer.validated_data['address'],
                        'phone_number': serializer.validated_data['phone_number']
                    }
                )
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            logout(request)  # Django's logout method will clear the session
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request):
        # Get the current authenticated user
        user = request.user
        # Get or create a UserProfile instance for the user
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Serialize the profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        # Get the current authenticated user
        user = request.user
        # Get or create a UserProfile instance for the user
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Deserialize the data to update the profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            # Save the updated profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)