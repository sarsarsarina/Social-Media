from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import NotFound, ValidationError

from apps.posts.models import Post
from apps.posts.selectors import get_post_by_id

from .models import Comment
from .selectors import get_comment_by_id


def create_comment(user, post_id, validated_data):
    post = get_post_by_id(post_id)

    if not post:
        raise NotFound("Post not found")

    if post.comments_enabled:
        raise ValidationError("Comments are disabled  for this post")

    parent = None
    parent_id = validated_data.get('parent')

    if parent_id:
        parent = get_comment_by_id(parent_id)
        
        if not parent or parent.post_id != post.id:
            raise ValidationError("Invalid parent comment")

    with transaction.atomic():
        comment = Comment.objects.create(
            post=post,
            user=user,
            parent=parent,
            content=validated_data['content']
        )

        Post.objects.filter(id=post_id).update(comments_count=F('comments_count') + 1)

    return comment
