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
        

class CreatePostSerializer(serializers.Serializer):
    caption = serializers.CharField(
        required=False, allow_blank=True
    )
    visibility = serializers.ChoiceField(
        choices=Post.Visibility.choices, default=Post.Visibility.PUBLIC
    )
    comments_enabled = serializers.BooleanField(
        default=True
    )
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )
    videos = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )