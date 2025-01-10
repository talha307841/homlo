from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id', 'owner', 'name', 'description', 'location',
            'price_per_night', 'available', 'image',
            'breakfast_included', 'lunch_included', 'dinner_included',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
