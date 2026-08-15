from django.db import models

class Follow(models.Model):
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
        default = "Pending"
    )
    is_close_friend = models.BooleanField(default = False)
    is_muted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    
def __str__(self):
    return f"{self.follower},{self.status},{self.following}"