from django.db import transaction
from django.db.models import F
from django.db.models.functions import Greatest
from rest_framework.exceptions import NotFound, ValidationError

from apps.posts.models import Post
from apps.posts.selectors import get_post_by_id

from .models import Comment
from .selectors import get_comment_by_id, post_comments_list, comment_replies

ALLOWED_COMMENT_ORDERINGS = ('-created_at', 'created_at')


def create_comment(user, post_id, validated_data):
    post = get_post_by_id(post_id)

    if not post:
        raise NotFound("Post not found")

    if not post.comments_enabled:
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


def update_comment(user, comment_id, validated_data):
    comment = get_comment_by_id(comment_id)

    if not comment or comment.user != user:
        raise NotFound("Comment not found")

    comment.content = validated_data['content']
    comment.is_edited = True
    comment.save(update_fields=['content', 'is_edited', 'updated_at'])

    return comment


def delete_comment(user, comment_id):
    comment = get_comment_by_id(comment_id)

    if not comment:
        raise NotFound("Comment not found")

    is_author = comment.user_id == user.id
    is_post_owner = comment.post.owner_id == user.id

    if not (is_author or is_post_owner):
        raise NotFound("Comment not found")

    with transaction.atomic():
        post_id = comment.post_id
        _, deleted_per_model = comment.delete()
        deleted_comments = deleted_per_model.get(Comment._meta.label, 0)

        Post.objects.filter(id=post_id).update(
            comments_count=Greatest(F('comments_count') - deleted_comments, 0)
        )


def get_post_comments(post_id, ordering='-created_at'):
    post = get_post_by_id(post_id)

    if not post:
        raise NotFound("Post not found")

    return post_comments_list(post_id, ordering)


def get_comment_replies(comment_id):
    comment = get_comment_by_id(comment_id)

    if not comment:
        raise NotFound("Comment not found")

    return comment, comment_replies(comment_id)

