from .models import User, UserProfile, Follow, FollowRequest, BlockUser, RestrictUser
from django.db.models import Q, Model


def get_user(email_or_username):
    return User.objects.filter(email=email_or_username).first() or \
        User.objects.filter(username=email_or_username).first()


def get_profile_by_user(user):
    profile = UserProfile.objects.get(user=user)
    return profile


def follow_exists(follower, following):
    exists = Follow.objects.filter(
        follower=follower,
        following=following
    ).exists()
    return exists


def get_user_by_id(user_id):
    return User.objects.filter(id=user_id).first()


def get_user_profile_by_id(user_id):
    return UserProfile.objects.select_related("user").filter(
        user_id=user_id
    ).first()


def followers_list(user):
    followers = Follow.objects.filter(following=user).order_by('-created_at')
    return followers


def following_list(user):
    following = Follow.objects.filter(follower=user).order_by('-created_at')
    return following


def follow_request_exists(from_user, to_user):
    request_exists = FollowRequest.objects.filter(
        from_user=from_user,
        to_user=to_user
    ).exists()
    return request_exists


def block_exists(blocker,blocked):
    block_exists = BlockUser.objects.filter(
        blocker = blocker,
        blocked = blocked
    ).exists()
    return block_exists


def is_blocked(user1, user2):
    is_blocked = BlockUser.objects.filter(
        Q(blocker = user1, blocked = user2) | Q(blocker = user2, blocked = user1)
    ).exists()
    return is_blocked


def followers_count(user_id):
    count = Follow.objects.filter(
        following = user_id
    ).count()
    return count


def following_count(user_id):
    count = Follow.objects.filter(
        follower = user_id
    ).count()
    return count


def restrict_exists(user, restricted_user):
    restrict_exists = RestrictUser.objects.filter(
        user = user,
        restricted_user = restricted_user
    ).exists()
    return restrict_exists