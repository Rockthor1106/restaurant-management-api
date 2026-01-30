from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from .models import OrderItem

from .services import delete_order_item

from .selectors import get_order_items, get_order_items_by_user

from .serializers import OrderItemCreateSerializer, OrderItemDetailSerializer, OrderItemUpdateSerializer


class OrderItemViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return get_order_items()
        return get_order_items_by_user(user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderItemCreateSerializer
        if self.action in ['update', 'partial_update']:
            return OrderItemUpdateSerializer
        return OrderItemDetailSerializer

    def perform_destroy(self, instance: OrderItem):
        delete_order_item(instance)


        
    
     

    

    
