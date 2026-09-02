from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .selectors import get_user, get_user_profile, follow_exists
from rest_framework.exceptions import ValidationError
from .models import Follow

User = get_user_model()


def create_user(validated_data):
    user = User.objects.create_user(**validated_data)

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    data = {
        'access': str(access),
        'refresh': str(refresh),
    }

    return data


def login_user(email_or_username=None, password=None):
    user = get_user(email_or_username)

    if user is None or not user.check_password(password):
        return None

    if not user.is_active:
        return None

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


def logout_user(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return {
            "message": "خروج موفقیت‌آمیز"
        }

    except Exception:
        return {
            "error": "توکن نامعتبر یا منقضی شده است"
        }


def update_profile(user, validated_data):
    profile = get_user_profile(user)

    if 'name' in validated_data:
        user.name = validated_data['name']
        user.save()

    if 'bio' in validated_data:
        profile.bio = validated_data['bio']
        profile.save()

    if 'avatar' in validated_data:
        profile.bio = validated_data['avatar']
        profile.save()


def follow_user(follower, following):
    if follower == following:
        raise ValidationError('You cant follow yourself')

    if follow_exists(follower, following):
        raise ValidationError('You already follow this user.')

    return create_follow(follower, following)


def create_follow(follower, following):
    follow = Follow.objects.create(
        follower=follower,
        following=following
    )
    return follow
