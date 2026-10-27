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
    
    
class PostMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "I", "Image"
        VIDEO = "V", "Video"
        
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media'
    )
    file = models.FileField(
        upload_to='posts/'
    )  
    media_type = models.CharField(
        max_length=2,
        choices=MediaType.choices,
        default=MediaType.IMAGE
    ) 
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.post} - {self.media_type} ({self.order})"


class SavedPost(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name = 'unique_saved_post_per_user'
            )
        ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_posts'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='saved_posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)