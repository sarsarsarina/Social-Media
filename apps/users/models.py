from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 150)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField(max_length = 128)
    phone_number = models.CharField(max_length = 15)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = False)
    is_private = models.BooleanField(default = False)
    last_login_ip = models.GenericIPAddressField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
def __str__(self):
    return self.username



