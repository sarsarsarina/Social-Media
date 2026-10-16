from rest_framework import serializers
from .models import Like
from apps.users.serializers import UserProfileSerializer


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id',
            'post',
            'comment',
            'created_at'
        ]


class PostLikesListSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='user.userprofile')

    class Meta:
        model = Like
        fields = ['profile']