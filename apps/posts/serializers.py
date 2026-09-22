from rest_framework import serializers
from .models import Post, PostMedia

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
    
    
class UpdatePostSerializer(serializers.Serializer):
    caption = serializers.CharField(
        required=False, allow_blank=True
    )
    visibility = serializers.ChoiceField(
        choices=Post.Visibility.choices, required=False
    )
    comments_enabled = serializers.BooleanField(
        required=False
    )
    new_images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )
    new_videos = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )
    remove_media_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    
    
class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = [
            'id',
            'file',
            'media_type',
            'order',
        ]
        

class PostDetailSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, read_only=True)
    
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
            'media'    
        ]