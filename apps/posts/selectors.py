from django.db.models import Q
from apps.users.models import BlockUser, Follow
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


def explore_posts():
    posts = Post.objects.filter(
        visibility=Post.Visibility.PUBLIC
    ).order_by('-created_at')

    return posts


def feed_posts(user, ordering='-created_at'):
    accepted_follows = Follow.objects.filter(
        follower=user,
        status=Follow.Status.ACCEPTED
    )
    following_ids = accepted_follows.values('following_id')
    close_friend_ids = accepted_follows.filter(is_close_friend=True).values('following_id')

    blocked_by_me = BlockUser.objects.filter(blocker=user).values('blocked_id')
    blocked_me = BlockUser.objects.filter(blocked=user).values('blocker_id')

    posts = (
        Post.objects.filter(
            Q(owner_id__in=following_ids,
              visibility__in=[Post.Visibility.PUBLIC, Post.Visibility.FOLLOWERS])
            | Q(owner_id__in=close_friend_ids,
                visibility=Post.Visibility.CLOSE_FRIENDS)
        )
        .exclude(owner_id__in=blocked_by_me)
        .exclude(owner_id__in=blocked_me)
        .select_related('owner')
        .prefetch_related('media')
        .order_by(ordering)
    )
    return posts
