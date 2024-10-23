from rest_framework.test import APITestCase
from core.models import User, Shop, Product, Category, Review, Order, WishList
from user.serializers import (
    UserSerializer, LoginSerializer, ShopSerializer,
    ProductSerializer, CategorySerializer, ReviewSerializer,
    OrderSerializer, WishListSerializer
)
from django.urls import reverse


class UserSerializerTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'Password123!',
            'user_age': 25
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_create_user_password_hashed(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertNotEqual(user.password, self.user_data['password'])  # Password should be hashed


class LoginSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='Password123!')

    def test_login_user(self):
        data = {'email': 'testuser@example.com', 'password': 'Password123!'}
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_invalid_credentials(self):
        data = {'email': 'testuser@example.com', 'password': 'wrongpassword'}
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ShopSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='shopowner@example.com', username='shopowner', password='Password123!')
        self.shop_data = {
            'shop_name': 'Test Shop',
            'shop_owner': self.user
        }

    def test_create_shop(self):
        serializer = ShopSerializer(data=self.shop_data)
        self.assertTrue(serializer.is_valid())
        shop = serializer.save()
        self.assertEqual(shop.shop_name, self.shop_data['shop_name'])
        self.assertEqual(shop.shop_owner, self.user)


class ProductSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='shopowner@example.com', username='shopowner', password='Password123!')
        self.shop = Shop.objects.create(shop_name='Test Shop', shop_owner=self.user)
        self.category = Category.objects.create(name='Electronics')
        self.product_data = {
            'product_name': 'Test Product',
            'short_description': 'Test short description',
            'long_description': 'Test long description',
            'price': 99.99,
            'quantity_available': 10,
            'shop': self.shop.id,
            'category': self.category.id
        }

    def test_create_product(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.product_name, self.product_data['product_name'])

    def test_create_product_invalid_data(self):
        invalid_product_data = {
            'product_name': 'Invalid Product',
            'short_description': 'No price here',
            'quantity_available': 10,
            'shop': self.shop.unique_id,
            'category': self.category.id
        }
        serializer = ProductSerializer(data=invalid_product_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
