from rest_framework import status

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.viewsets import ModelViewSet

from .selectors import get_products, get_active_products

from .services import activate_product, deactivate_product

from .serializers import ProductCreateSerializer, ProductDetailSerializer


class ProductViewSet(ModelViewSet):

    def get_queryset(self):
        return get_products()

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return ProductDetailSerializer

    def get_permissions(self):
        if self.action in [
            'create',
            'update',
            'partial_update',
            'destroy', 
            'activate',
            'deactivate'
        ]:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=['POST'], detail=True)
    def activate(self, request, pk=None):
        product = self.get_object()

        activate_product(product, request.user)

        serializer = self.get_serializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def deactivate(self, request, pk=None):
        product = self.get_object()

        deactivate_product(product, request.user)
        
        serializer = self.get_serializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def active(self, request):
        products = get_active_products()

        serializer = self.get_serializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

