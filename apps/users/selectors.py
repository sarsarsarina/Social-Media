from .models import User

def get_user(email):
    return User.objects.filter(email = email).first()