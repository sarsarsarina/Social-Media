from django.conf import settings
from django.db import models
from apps.posts.models import Post

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = "comments",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        on_delete = models.CASCADE,
        related_name = "replies",
        null =  True,
        blank = True,
    )
    content = models.TextField()
    is_edited = models.BooleanField(
        default = False,
    )
    created_at = models.DateTimeField(
        auto_now_add = True,
    )
    updated_at = models.DateTimeField(
        auto_now = True,
    )

    def __str__(self):
        return f"{self.user} - {self.content[:20]} (#{self.pk})"