from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(validated_data):
    return User.objects.create_user(**validated_data)

