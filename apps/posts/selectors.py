from .models import Post

def my_posts(user):
    posts = Post.objects.filter(owner=user).order_by('-created_at')
    return posts

def get_post_by_id(post_id):
    return Post.objects.filter(id=post_id).first()