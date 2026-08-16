from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length = 15)
    is_verified = models.BooleanField(default = False)
    is_private = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Follow(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = "A"
        REJECTED = "R"
        PENDING = "P"
        
    follower = models.ForeignKey(
        "users.User",
        on_delete = models.CASCADE,
        related_name = "following"
    )
    following = models.ForeignKey(
        "users.User",
        on_delete = models.CASCADE,
        related_name = "followers"
    )
    status = models.CharField(
        max_length = 20,
        default = Status.PENDING,
        choices = Status.choices
    )
    is_close_friend = models.BooleanField(default = False)
    is_muted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.follower},{self.status},{self.following}"



