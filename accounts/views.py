from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .selectors import get_users

from .serializers import UserCreateSerializer, UserListSerializer


class UserViewSet(ModelViewSet):

    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return get_users()