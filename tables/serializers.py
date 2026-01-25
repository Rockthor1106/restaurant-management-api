from rest_framework import serializers

from .models import Table

class TableCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = [
            'number',
            'capacity',
        ]

class TableDetailSerializer(serializers.ModelSerializer):

    number = serializers.ReadOnlyField()
    capacity = serializers.ReadOnlyField()
    has_active_order = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Table
        fields = [
            'number',
            'capacity',
            'has_active_order',
            'created_at',
            'updated_at',
            'is_active',
        ]

class TableUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = [
            'capacity',
            'is_active'
        ]