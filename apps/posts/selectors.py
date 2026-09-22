from .models import Post

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