from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelTests(TestCase):
    """Tests for the User model."""

    def test_create_user_success(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='Testpass123!'
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.username, 'testuser')

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='testuser', password='Testpass123!')

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='testuser@example.com', username='', password='Testpass123!')

    def test_create_user_with_valid_password(self):
        user = User.objects.create_user(
            email='validuser@example.com',
            username='validuser',
            password='ValidPass123!'
        )
        self.assertTrue(user.check_password('ValidPass123!'))

    def test_create_user_with_invalid_password(self):
        with self.assertRaises(ValidationError):
            user = User(email='testuser@example.com', username='testuser')
            user.set_password('short')
            user.full_clean()  # Triggers validation

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='Superpass123!'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_is_active_by_default(self):
        user = User.objects.create_user(
            email='activeuser@example.com',
            username='activeuser',
            password='Activepass123!'
        )
        self.assertTrue(user.is_active)

    def test_user_orders_completed_default(self):
        user = User.objects.create_user(
            email='ordersuser@example.com',
            username='ordersuser',
            password='Orderspass123!'
        )
        self.assertEqual(user.orders_completed, 0)

    def test_user_wish_list_default(self):
        user = User.objects.create_user(
            email='wishlistuser@example.com',
            username='wishlistuser',
            password='Wishlistpass123!'
        )
        self.assertEqual(user.wish_list, [])

    def test_user_address_default(self):
        user = User.objects.create_user(
            email='addressuser@example.com',
            username='addressuser',
            password='Addresspass123!'
        )
        self.assertEqual(user.address, [])
