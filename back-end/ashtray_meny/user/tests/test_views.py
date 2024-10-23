from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status  # Added import
from core.models import User, Shop, Product, Category


class UserViewSetTests(APITestCase):
    """
    Test the UserViewSet functionality, including authentication and permission handling.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', username='user', password='Password123!')
        self.client.force_authenticate(user=self.user)  # Authenticate client for authenticated requests
        self.user_data = {'email': 'newuser@example.com', 'username': 'newuser', 'password': 'Password123!'}

    def test_list_users_authenticated(self):
        """Test listing users as an authenticated user."""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_users_unauthenticated(self):
        """Test listing users as an unauthenticated user should fail."""
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_with_invalid_data(self):
        """Test creating a user with invalid data should fail (e.g., missing fields)."""
        invalid_user_data = {'email': 'invalid@example.com'}  # Missing required fields
        url = reverse('user-list')
        response = self.client.post(url, data=invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductViewSetTests(APITestCase):
    """
    Test the ProductViewSet functionality, ensuring correct permission and data validation
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='shopowner@example.com', username='shopowner', password='Password123!')
        self.client.force_authenticate(user=self.user)
        self.shop = Shop.objects.create(shop_name='Test Shop', shop_owner=self.user)
        self.category = Category.objects.create(name="Electronics")  # Fixed category name field
        self.product_data = {
            'product_name': 'Product1',
            'short_description': 'Short description',
            'long_description': 'Long description',
            'price': '10.99',
            'quantity_available': 50,
            'shop': self.shop.unique_id,  # Fixed shop to use unique_id
            'category': self.category.unique_id  # Fixed category to use unique_id
        }

    def test_create_product_authenticated(self):
        """Test creating a product as an authenticated user should succeed."""
        url = reverse('product-list')
        response = self.client.post(url, data=self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_name'], self.product_data['product_name'])

    def test_create_product_unauthenticated(self):
        """Test creating a product as an unauthenticated user should fail."""
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('product-list')
        response = self.client.post(url, data=self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_invalid_data(self):
        """Test creating a product with invalid data (missing fields) should fail."""
        invalid_product_data = {'product_name': 'Product without price'}  # Missing required fields
        url = reverse('product-list')
        response = self.client.post(url, data=invalid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
