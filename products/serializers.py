from rest_framework import serializers

from rest_framework.exceptions import ValidationError

from .models import Product

class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'name',
            'price'
        ]

    def validate_price(self, price):
        if price < 0:
            raise ValidationError('Price cannot be a negative value')
        return price

class ProductDetailSerializer(serializers.ModelSerializer):

    created_by = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta: 
        model = Product
        fields = [
            'name',
            'price',
            'is_active',
            'created_by',
            'created_at',
            'updated_at',
        ]