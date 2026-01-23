from rest_framework import status

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsRestaurantAdmin

from .selectors import get_orders

from .serializers import OrderCreateSerializer, OrderDetailSerializer

from .services import start_preparation, mark_ready, deliver, pay_order, cancel_order


class OrderViewSet(ModelViewSet):

    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_orders()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsRestaurantAdmin()]
        return super().get_permissions()

    @action(methods=['POST'], detail=True)
    def prepare(self, request, pk=None):
        order = self.get_object()
        start_preparation(order)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def ready(self, request, pk=None):
        order = self.get_object()
        mark_ready(order)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def deliver(self, request, pk=None):
        order = self.get_object()
        deliver(order)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def pay(self, request, pk=None):
        order = self.get_object()
        pay_order(order)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def cancel(self, request, pk=None):
        order = self.get_object()
        cancel_order(order)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

    
    

    