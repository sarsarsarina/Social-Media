from apps.posts.models import Post
from apps.likes.models import Like


def get_post_by_id(post_id):
    return Post.objects.filter(id=post_id).first()

def like_exists(user, post):
    like_exists = Like.objects.filter(
        user=user,
        post=post
    ).exists()
    return like_exists


def get_like(user, post):
    like = Like.objects.filter(
        user=user,
        post=post
    ).first()
    return like