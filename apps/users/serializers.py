from rest_framework import serializers
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "username",
            "password",
            "phone_number"
        ]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "password": {"required": True, "write_only": True},
            "phone_number": {"required": True}
        }


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()