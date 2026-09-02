from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

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
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        if not data.get("email_or_username"):
            raise serializers.ValidationError(
                "Email or username is required."
            )
        return data
    
    
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required = True)

    
class MyUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "avatar", "website", "gender", "birth_date", "location"]

    
class MyProfileSerializer(serializers.ModelSerializer):
    userprofile = MyUserProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "phone_number", "userprofile"]
        

