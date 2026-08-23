from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
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


def login_user(email, username, password):
    
    if email:
        user = get_user(email)
        
        if user:
            user = authenticate(
                username = username,
                password = password
            )
    
    elif username:
        user = authenticate(
            username = username,
            password = password
        )
        
    else:
        user = None
        
    if user is None:
        return None
    
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    
    return ({
        'access' : str(access),
        'refresh' : str(refresh),
    })