from .models import User, UserProfile, Follow


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





