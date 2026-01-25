from rest_framework import status

from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from .selectors import get_tables, get_available_tables

from .serializers import TableDetailSerializer, TableCreateSerializer, TableUpdateSerializer

from .services import activate_table, deactivate_table


class TableViewSet(ModelViewSet):

    def get_queryset(self):
        return get_tables()

    def get_serializer_class(self):
        if self.action == 'create':
            return TableCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TableUpdateSerializer
        return TableDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'available']: 
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser()]

    @action(methods=['POST'], detail=True)
    def activate(self, request, pk=None):
        table = self.get_object()
        activate_table(table, request.user)
        serializer = TableDetailSerializer(table)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def deactivate(self, request, pk=None):
        table = self.get_object()
        deactivate_table(table, request.user)
        serializer = TableDetailSerializer(table)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def available(self, request):
        available_tables = get_available_tables()
        serializer = self.get_serializer(available_tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)