from rest_framework import viewsets, permissions, generics
from core.models import User, Shop, Product, Category, Review, Order, WishList
from user.serializers import (
    UserSerializer, ShopSerializer, ProductSerializer, CategorySerializer,
    ReviewSerializer, OrderSerializer, WishListSerializer, LoginSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt  # <-- Add this import
from django.utils.decorators import method_decorator

# User Registration View
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system (Registration)."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]  # No authentication required for registration


@method_decorator(csrf_exempt, name='dispatch')  # <-- Properly apply csrf_exempt
class LoginView(generics.GenericAPIView):
    """Login view that returns JWT tokens upon valid email and password."""
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.unique_id,
        })

# User ViewSet (CRUD, requires authentication)
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user CRUD operations."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'unique_id'  # Use unique_id instead of default pk

    def update(self, request, *args, **kwargs):
        """Custom update method to handle password hashing and user updates."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # If 'password' is provided in the request, hash it before saving
        if 'password' in request.data:
            instance.set_password(request.data['password'])
            request.data.pop('password')

        # Check if 'user_shop' is provided in the request and update it
        if 'user_shop' in request.data:
            instance.user_shop_id = request.data['user_shop']  # Update user_shop

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Other ViewSets...

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

class WishListViewSet(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    queryset = WishList.objects.all()
    permission_classes = [IsAuthenticated]
