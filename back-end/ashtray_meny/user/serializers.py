from rest_framework import serializers
from core.models import User, Shop, Product, Category, Review, Order, WishList
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _




# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'unique_id', 'email', 'username', 'user_image', 'user_age', 
            'is_verified', 'is_staff', 'shop_owner', 'default_address', 
            'orders_completed', 'orders_now', 'about_user', 'password'
        ]  # Include all the required fields
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Override the default create method to handle password hashing."""
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user



class LoginSerializer(serializers.Serializer):
    """Serializer for logging in a user using JWT tokens."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user using email and password."""
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate user using email
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            msg = _('Unable to authenticate with the provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        # Add the user to the validated data
        attrs['user'] = user
        return attrs




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
