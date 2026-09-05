from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .selectors import (
    get_user,
    get_user_by_id,
    get_profile_by_user,
    get_user_profile_by_id,
    follow_exists,
)
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from .models import UserProfile, Follow

User = get_user_model()


def create_user(validated_data):
    user = User.objects.create_user(**validated_data)
    UserProfile.objects.create(user=user)

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    data = {
        'access': str(access),
        'refresh': str(refresh),
    }

    return data


def login_user(email_or_username=None, password=None):
    user = get_user(email_or_username)

    if user is None or not user.check_password(password) or not user.is_active:
        raise AuthenticationFailed("Invalid email/username or password")

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


def logout_user(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

    except Exception:
        raise ValidationError("Invalid or expired token")

    return {
        "message": "Successfully logged out"
    }


def update_profile(user, validated_data):
    profile = get_profile_by_user(user)

    if 'name' in validated_data:
        user.name = validated_data['name']
        user.save()

    if 'bio' in validated_data:
        profile.bio = validated_data['bio']
        profile.save()

    if 'avatar' in validated_data:
        profile.avatar = validated_data['avatar']
        profile.save()

    return profile


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


def get_my_profile(user_id):
    return User.objects.select_related("userprofile").filter(id=user_id).first()


def get_user_profile(user_id):
    user = get_user_by_id(user_id)
    if not user:
        raise NotFound("User not found")

    profile = get_user_profile_by_id(user_id)
    if not profile:
        raise NotFound("Profile not found")

    return profile
