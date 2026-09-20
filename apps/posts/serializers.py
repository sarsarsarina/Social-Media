from rest_framework import serializers
from .models import Post

class MyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'caption',
            'visibility',
            'comments_enabled',
            'likes_count',
            'comments_count',
            'created_at',
        ]