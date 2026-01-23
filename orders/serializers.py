from rest_framework import serializers

from .models import Order

class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'table'
        ]

class OrderDetailSerializer(serializers.ModelSerializer):

    table = serializers.SerializerMethodField(read_only=True)
    status = serializers.ReadOnlyField()
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            'table',
            'status',
            'created_by',
            'created_at',
            'updated_at'
        ]

    def get_table(self, obj):
        return {
            'id': obj.table.id,
            'number': obj.table.number
        }

