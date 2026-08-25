from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from .selectors import get_user

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
        return{
            "message": "خروج موفقیت‌آمیز"
        }  

    except Exception:
        return{
            "error": "توکن نامعتبر یا منقضی شده است"
        }