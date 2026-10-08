from rest_framework import serializers

from .models import Comment


class CreateCommentSerializer(serializers.Serializer):
    content = serializers.CharField()
    parent = serializers.IntegerField(required=False, allow_null=True)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'parent',
            'content',
            'is_edited',
            'created_at',
        ]