from rest_framework import serializers
from core.models import User, Shop, Product, Category, Review, Order, WishList

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}


# Shop Serializer
class ShopSerializer(serializers.ModelSerializer):
    """Serializer for the shop object."""

    class Meta:
        model = Shop
        fields = '__all__'


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the product object."""

    class Meta:
        model = Product
        fields = '__all__'


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the category object."""

    class Meta:
        model = Category
        fields = '__all__'


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the review object."""

    class Meta:
        model = Review
        fields = '__all__'


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the order object."""

    class Meta:
        model = Order
        fields = '__all__'


# WishList Serializer
class WishListSerializer(serializers.ModelSerializer):
    """Serializer for the wishlist object."""

    class Meta:
        model = WishList
        fields = '__all__'
