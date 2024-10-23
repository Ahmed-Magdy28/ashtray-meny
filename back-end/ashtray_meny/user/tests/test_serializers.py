from rest_framework.test import APITestCase
from rest_framework import status  # Added import
from django.urls import reverse
from core.models import User, Shop, Product, Category, Review, Order, WishList
from user.serializers import (
    UserSerializer, LoginSerializer, ShopSerializer,
    ProductSerializer, CategorySerializer, ReviewSerializer,
    OrderSerializer, WishListSerializer
)

class UserSerializerTest(APITestCase):
    """
    Test the UserSerializer functionality, focusing on user creation and password handling.
    """

    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'Password123!',
            'user_age': 25
        }

    def test_create_user(self):
        """Test creating a user with valid data."""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_create_user_password_hashed(self):
        """Test that the password is hashed when creating a user."""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertNotEqual(user.password, self.user_data['password'])  # Password should be hashed


class LoginSerializerTest(APITestCase):
    """
    Test logging in users using the LoginSerializer.
    """

    def setUp(self):
        # Use a valid password that meets the strength criteria (with an uppercase letter)
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='Password123!')

    def test_login_user(self):
        """Test logging in a user with correct credentials."""
        data = {'email': 'testuser@example.com', 'password': 'Password123!'}
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_invalid_credentials(self):
        """Test logging in with invalid credentials should fail."""
        data = {'email': 'testuser@example.com', 'password': 'wrongpassword'}
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ShopSerializerTest(APITestCase):
    """
    Test the ShopSerializer, including data validation and shop creation.
    """

    def setUp(self):
        self.user = User.objects.create_user(email='shopowner@example.com', username='shopowner', password='Password123!')
        self.shop_data = {
            'shop_name': 'Test Shop',
            'shop_owner': self.user.unique_id  # Fixed shop_owner to use unique_id
        }

    def test_create_shop(self):
        """Test creating a shop with valid data."""
        serializer = ShopSerializer(data=self.shop_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Debugging validation errors
        shop = serializer.save()
        self.assertEqual(shop.shop_name, self.shop_data['shop_name'])
        self.assertEqual(shop.shop_owner, self.user)


class ProductSerializerTest(APITestCase):
    """
    Test the ProductSerializer, focusing on product creation and validation.
    """

    def setUp(self):
        self.user = User.objects.create_user(email='shopowner@example.com', username='shopowner', password='Password123!')
        self.shop = Shop.objects.create(shop_name='Test Shop', shop_owner=self.user)
        self.category = Category.objects.create(name='Electronics')  # Fixed category field name to match model
        self.product_data = {
            'product_name': 'Test Product',
            'short_description': 'Test short description',
            'long_description': 'Test long description',
            'price': 99.99,
            'quantity_available': 10,
            'shop': self.shop.unique_id,  # Fixed shop to use unique_id
            'category': self.category.unique_id,  # Fixed category to use unique_id
            'dimensions': '10x10x10 cm',  # Add missing field
            'weight': 1.5,  # Add missing field
            'image_1': None,  # Image field can be set to None for testing, or provide a mock image
        }


    def test_create_product_invalid_data(self):
        """Test creating a product with invalid data should fail (e.g., missing price)."""
        invalid_product_data = {
            'product_name': 'Invalid Product',
            'short_description': 'No price here',
            'quantity_available': 10,
            'shop': self.shop.unique_id,
            'category': self.category.unique_id
        }
        serializer = ProductSerializer(data=invalid_product_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)




class OrderSerializerTest(APITestCase):
    """
    Test the OrderSerializer, focusing on creating and validating orders.
    """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='Password123!')
        self.order_data = {
            'user': self.user.unique_id,
            'total_amount': 100.00
        }

    def test_create_order(self):
        """Test creating an order with valid data."""
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.total_amount, self.order_data['total_amount'])



