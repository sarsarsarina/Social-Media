from .models import User

def get_user(email_or_username):
    return User.objects.filter(email=email_or_username).first() or \
           User.objects.filter(username=email_or_username).first()
           
def get_user_by_id(user_id):
    return User.objects.filter(id = user_id).first()