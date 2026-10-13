from django.db import models
from django.conf import settings
from apps.posts.models import Post
from apps.comments.models import Comment
from django.db.models import Q


class Like(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                        Q(post__isnull=False, comment__isnull=True)
                        |
                        Q(post__isnull=True, comment__isnull=False)
                ),
                name='like_has_exactly_one_target',
            ),
            models.UniqueConstraint(
                fields=['user', 'post'],
                condition=Q(post__isnull=False),
                name='unique_user_post_like',
            ),
            models.UniqueConstraint(
                fields=['user', 'comment'],
                condition=Q(comment__isnull=False),
                name='unique_user_comment_like',
            ),
        ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='likes',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.post_id:
            return f"{self.user} liked post #{self.post_id}"
        return f"{self.user} liked comment #{self.comment_id}"