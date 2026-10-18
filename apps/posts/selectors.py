from .models import Post, SavedPost

def my_posts(user):
    posts = Post.objects.filter(owner=user).order_by('-created_at')
    return posts

def get_post_by_id(post_id):
    return Post.objects.filter(id=post_id).first()


def post_list(user_id=None, ordering='-created_at'):
    posts = Post.objects.all()
    
    if user_id:
        posts = posts.filter(owner_id=user_id)

    posts = posts.order_by(ordering)

    return posts


def explore_posts():
    posts = Post.objects.filter(
        visibility=Post.Visibility.PUBLIC
    ).order_by('-created_at')

    return posts


def is_post_saved(user, post):
    saved_post = SavedPost.objects.filter(
        user=user,
        post=post
    ).exists()
    return saved_post


def get_saved_post(user, post):
    saved_post = SavedPost.objects.filter(
        user=user,
        post=post
    ).first()
    return saved_post


def get_saved_posts(user):
    return Post.objects.filter(
        saved_posts__user=user
    ).order_by('-saved_posts__created_at')