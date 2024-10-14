from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import User
from core.validators import validate_password_strength
from django.db.utils import IntegrityError

class UserModelTest(TestCase):

    def setUp(self):
        self.valid_user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'ValidPass123!'
        }

    def test_create_user_success(self):
        """Test creating a user with valid data."""
        user = User.objects.create_user(
            email=self.valid_user_data['email'],
            username=self.valid_user_data['username'],
            password=self.valid_user_data['password']
        )
        self.assertEqual(user.email, self.valid_user_data['email'])
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertTrue(user.check_password(self.valid_user_data['password']))

    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without an email raises an error."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, username='user', password='ValidPass123!')

    def test_create_user_without_username_raises_error(self):
        """Test that creating a user without a username raises an error."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='user@example.com', username=None, password='ValidPass123!')

    def test_create_user_with_invalid_password_raises_error(self):
        """Test that creating a user with an invalid password raises ValidationError."""
        with self.assertRaises(ValidationError):
            User.objects.create_user(email='user@example.com', username='user', password='weakpass')

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(
            email=self.valid_user_data['email'],
            username=self.valid_user_data['username'],
            password=self.valid_user_data['password']
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_user_with_duplicate_email_raises_error(self):
        """Test that creating a user with an existing email raises an IntegrityError."""
        User.objects.create_user(
            email=self.valid_user_data['email'],
            username='user1',
            password='ValidPass123!'
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.valid_user_data['email'],
                username='user2',
                password='ValidPass123!'
            )

    def test_password_strength_requirements(self):
        """Test various invalid password scenarios."""
        invalid_passwords = {
            'no_uppercase': 'password123!',
            'no_lowercase': 'PASSWORD123!',
            'no_digit': 'Password!',
            'no_special_char': 'Password123',
            'too_short': 'Pass12!'
        }

        for case, pwd in invalid_passwords.items():
            with self.assertRaises(ValidationError, msg=f"Failed on: {case}"):
                validate_password_strength(pwd)

        # Test with valid password
        try:
            validate_password_strength('ValidPass123!')
        except ValidationError:
            self.fail('validate_password_strength() raised ValidationError unexpectedly!')