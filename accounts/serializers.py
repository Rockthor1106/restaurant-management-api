from rest_framework import serializers

from .models import User

from .services import create_user

class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
            return create_user(validated_data)

    def validate_username(self, username: str):
        if username.lower() != 'admin':
            return username
        raise serializers.ValidationError("Username not available")

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username']





        



