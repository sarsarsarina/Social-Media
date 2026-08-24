from .models import User

def get_user(email=None, username=None):
    qs = User.objects.none()
    if email:
        qs = User.objects.filter(email=email)
    if not qs.exists() and username:
        qs = User.objects.filter(username=username)
    return qs.first()