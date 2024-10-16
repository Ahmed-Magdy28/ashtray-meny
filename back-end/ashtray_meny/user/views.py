from rest_framework import viewsets, permissions
from core.models import User, Shop, Product, Category, Review, Order, WishList
from user.serializers import (
    UserSerializer, ShopSerializer, ProductSerializer, CategorySerializer,
    ReviewSerializer, OrderSerializer, WishListSerializer
)
from rest_framework.permissions import IsAuthenticated

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user CRUD operations."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


# Shop ViewSet
class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet for managing shops."""
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated]


# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for managing products."""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing categories."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]


# Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing reviews."""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for managing orders."""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]


# WishList ViewSet
class WishListViewSet(viewsets.ModelViewSet):
    """ViewSet for managing wishlists."""
    serializer_class = WishListSerializer
    queryset = WishList.objects.all()
    permission_classes = [IsAuthenticated]
