from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, Follow


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
    refresh_token = serializers.CharField(required=True)


class UpdateProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            'name',
            'bio',
            'avatar'
        ]


class MyUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "avatar", "website", "gender", "birth_date", "location"]


class MyProfileSerializer(serializers.ModelSerializer):
    userprofile = MyUserProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "phone_number", "userprofile"]


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id")
    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ["id", "username", "email", "avatar", "bio", "website"]


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following']


class FollowersListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='follower.username')
    bio = serializers.CharField(source='follower.userprofile.bio')
    avatar = serializers.CharField(source='follower.userprofile.avatar')

    class Meta:
        model = Follow
        fields = [
            'username',
            'bio',
            'avatar'
        ]


