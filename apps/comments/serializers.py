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


class UpdateCommentSerializer(serializers.Serializer):
    content = serializers.CharField()


class PostCommentsFilterSerializer(serializers.Serializer):
    ORDERING_MAP = {
        'newest': '-created_at',
        'oldest': 'created_at',
    }

    ordering = serializers.ChoiceField(
        choices=list(ORDERING_MAP.keys()),
        required=False,
        default='newest',
    )

    def validate_ordering(self, value):
        return self.ORDERING_MAP[value]

class PostCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    replies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'username',
            'content',
            'is_edited',
            'created_at',
            'replies_count',
        ]