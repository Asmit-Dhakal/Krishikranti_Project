# password_reset/serializers.py

from rest_framework import serializers

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        # You can add custom password validation here if needed
        return value
