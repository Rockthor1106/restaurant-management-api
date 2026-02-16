from rest_framework import serializers

from rest_framework.exceptions import ValidationError

from .models import OrderItem

from .services import create_order_item, update_order_item_quantity

class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'quantity',
        ]

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise ValidationError("Quantity must be at least 1")
        
        return quantity

    def create(self, validated_data):
        order = validated_data['order']
        product = validated_data['product']
        quantity = validated_data['quantity']
        
        return create_order_item(order, product, quantity)

    def validate_quantity(self, quantity):
            if quantity <= 0:
                raise ValidationError("Quantity must be at least 1")
            
            return quantity
            

class OrderItemDetailSerializer(serializers.ModelSerializer):
    
    order = serializers.IntegerField(source='order.pk', read_only=True)
    product = serializers.IntegerField(source='product.pk', read_only=True)
    product_name = serializers.ReadOnlyField()
    quantity = serializers.ReadOnlyField()
    unit_price = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'product_name',
            'unit_price',
            'quantity',
            'created_at',
            'updated_at',
        ]

class OrderItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'quantity'
        ]

    def validate_quantity(self, quantity):
            if quantity <= 0:
                raise ValidationError("Quantity must be at least 1")
            
            return quantity

    def update(self, order_item, validated_data):
        quantity = validated_data['quantity']

        return update_order_item_quantity(order_item, quantity)



