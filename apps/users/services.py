from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

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
