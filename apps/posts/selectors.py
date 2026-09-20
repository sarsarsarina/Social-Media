from .models import Post

def my_posts(user):
    post = Post.objects.filter(user=owner).ordered_by('-created_at')
    return post