from rest_framework import serializers
from core.models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'short_description', 
            'long_description', 'price', 'quantity_available', 
            'shop', 'category', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

