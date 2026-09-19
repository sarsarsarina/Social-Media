from django.db import models
from django.conf import settings

class Post(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "P", "Public"
        FOLLOWERS = "F", "Followers"
        CLOSE_FRIENDS = "CF", "Close Friends"
        ONLY_ME = "O", "Only You"
        
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    caption = models.TextField(
        blank=True, null=True
    )
    visibility = models.CharField(
        max_length=2,
        choices=Visibility.choices,
        default=Visibility.PUBLIC
    )
    comments_enabled = models.BooleanField(default=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.owner} - {self.caption[:20]} ({self.created_at.strftime('%Y-%m-%d')})"