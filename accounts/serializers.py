from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    address = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'address', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'address': {'required': True},
            'phone_number': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'address': validated_data['address'],
                'phone_number': validated_data['phone_number']
            }
        )
        return user



class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', write_only=True)
    last_name = serializers.CharField(source='user.last_name', write_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number']

    def update(self, instance, validated_data):
        # Extract user data
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            # Update user fields
            if 'first_name' in user_data:
                user.first_name = user_data['first_name']
            if 'last_name' in user_data:
                user.last_name = user_data['last_name']
            user.save()

        # Update profile fields
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if old_password == new_password:
            raise serializers.ValidationError({'new_password': 'New password must be different from old password.'})

        return attrs

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})

        return old_password