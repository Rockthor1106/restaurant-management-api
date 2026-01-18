from .models import User

def get_users():
    return User.objects.all()