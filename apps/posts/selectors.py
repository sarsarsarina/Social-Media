from .models import Post

def my_posts(user):
    posts = Post.objects.filter(owner=user).order_by('-created_at')
    return posts