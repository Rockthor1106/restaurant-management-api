from rest_framework import serializers

from .models import Table

class TableSerializer(serializers.ModelSerializer):

    available = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = [
            'number',
            'capacity',
            'available',
            'created_at',
            'updated_at'
        ]

    def get_available(self, obj):
        return bool(obj.orders.filter(is_active==True))


