from .models import User, UserProfile, Follow


def get_user(email_or_username):
    return User.objects.filter(email=email_or_username).first() or \
        User.objects.filter(username=email_or_username).first()


def get_user_profile(user):
    profile = UserProfile.objects.get(user=user)
    return profile


def follow_exists(follower, following):
    exists = Follow.objects.filter(follower=follower, following=following).exists()
    return exists
