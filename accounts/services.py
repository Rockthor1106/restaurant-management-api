from .models import User

def create_user(validated_data):
    return User.objects.create_user(**validated_data)
