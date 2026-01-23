from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.viewsets import ModelViewSet

from .permissions import IsStaff

from .selectors import get_tables
from .serializers import TableSerializer

class TableViewSet(ModelViewSet):

    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_tables()

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [IsAdminUser]
    #     elif self.action in ['list', 'retrieve']:
    #         return [IsStaff]
    #     return super().get_permissions()

    # @action(methods=['PUT'], detail=True, url_path='assign-orde-to-table')
    # def assign_order_to_table(self, request):
    #     table = self.get_object()
    #     serializer = TableSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()


