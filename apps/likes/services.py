from apps.likes.models import Like
from apps.posts.models import Post
from .selectors import like_exists
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import F


def like_post(user, post):
    if like_exists(user, post):
        raise ValidationError('You have already liked this post.')

    with transaction.atomic():
        like = create_like(user, post)

        Post.objects.filter(pk=post.pk).update(
            likes_count=F('likes_count') + 1
        )
        return like


def create_like(user, post):
    like = Like.objects.create(
        user=user,
        post=post
    )
    return like
