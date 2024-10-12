from django.test import TestCase  # Django's built-in test framework.
from django.core.exceptions import ValidationError  # For handling validation errors.
from django.utils import timezone  # To manage timestamps.
from .models import User, Shop, Product, Category, Order, Review  # Import models to be tested.

class UserModelTest(TestCase):
    """Tests for the User model."""

    def setUp(self):
        """Create a sample user for testing."""
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user1',
            password='securepassword123'
        )

    def test_create_user(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.email, 'user@example.com')
        self.assertTrue(self.user.check_password('securepassword123'))
        self.assertFalse(self.user.is_staff)

    def test_create_superuser(self):
        """Test that a superuser is created with the correct permissions."""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='supersecurepassword123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_image_validation(self):
        """Test that invalid image types raise a validation error."""
        with self.assertRaises(ValidationError):
            self.user.user_image = 'invalid_image.txt'  # Assign invalid image type.
            self.user.full_clean()  # Triggers validation.

class ShopModelTest(TestCase):
    """Tests for the Shop model."""

    def setUp(self):
        """Create a sample user and shop for testing."""
        self.user = User.objects.create_user(
            email='shopowner@example.com',
            username='shopowner',
            password='password123'
        )
        self.shop = Shop.objects.create(
            shop_name='Test Shop',
            shop_owner=self.user
        )

    def test_create_shop(self):
        """Test that a shop is created successfully."""
        self.assertEqual(self.shop.shop_name, 'Test Shop')
        self.assertEqual(self.shop.shop_owner, self.user)

    def test_shop_identity_colors_validation(self):
        """Test that more than 3 identity colors raise a validation error."""
        self.shop.shop_identity_colors = ['#FFFFFF', '#000000', '#FF5733', '#FF5734']
        with self.assertRaises(ValidationError):
            self.shop.full_clean()  # Triggers validation.

class ProductModelTest(TestCase):
    """Tests for the Product model."""

    def setUp(self):
        """Create sample data for testing."""
        self.user = User.objects.create_user(
            email='shopowner@example.com',
            username='shopowner',
            password='password123'
        )
        self.shop = Shop.objects.create(
            shop_name='Test Shop',
            shop_owner=self.user
        )
        self.category = Category.objects.create(
            name='Electronics'
        )
        self.product = Product.objects.create(
            product_name='Smartphone',
            short_description='Latest model',
            long_description='A very advanced smartphone.',
            price=699.99,
            quantity_available=50,
            dimensions='6x3x0.3 inches',
            weight=0.5,
            shop=self.shop,
            category=self.category
        )

    def test_create_product(self):
        """Test that a product is created successfully."""
        self.assertEqual(self.product.product_name, 'Smartphone')
        self.assertEqual(self.product.price, 699.99)
        self.assertEqual(self.product.shop, self.shop)

    def test_product_quantity_validation(self):
        """Test that negative quantities raise a validation error."""
        self.product.quantity_available = -1
        with self.assertRaises(ValidationError):
            self.product.full_clean()  # Triggers validation.

class OrderModelTest(TestCase):
    """Tests for the Order model."""

    def setUp(self):
        """Create sample data for testing orders."""
        self.user = User.objects.create_user(
            email='customer@example.com',
            username='customer',
            password='password123'
        )
        self.shop = Shop.objects.create(
            shop_name='Test Shop',
            shop_owner=self.user
        )
        self.category = Category.objects.create(
            name='Electronics'
        )
        self.product = Product.objects.create(
            product_name='Smartphone',
            short_description='Latest model',
            long_description='A very advanced smartphone.',
            price=699.99,
            quantity_available=50,
            shop=self.shop,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=699.99,
            order_status='pending'
        )
        self.order.products.add(self.product)

    def test_create_order(self):
        """Test that an order is created successfully."""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.total_amount, 699.99)
        self.assertEqual(self.order.products.count(), 1)

    def test_order_status_update(self):
        """Test that the order status can be updated."""
        self.order.order_status = 'completed'
        self.order.save()
        self.assertEqual(self.order.order_status, 'completed')

class ReviewModelTest(TestCase):
    """Tests for the Review model."""

    def setUp(self):
        """Create sample data for testing reviews."""
        self.user = User.objects.create_user(
            email='customer@example.com',
            username='customer',
            password='password123'
        )
        self.shop = Shop.objects.create(
            shop_name='Test Shop',
            shop_owner=self.user
        )
        self.product = Product.objects.create(
            product_name='Smartphone',
            short_description='Latest model',
            long_description='A very advanced smartphone.',
            price=699.99,
            quantity_available=50,
            shop=self.shop,
            category=Category.objects.create(name='Electronics')
        )
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Excellent product!'
        )

    def test_create_review(self):
        """Test that a review is created successfully."""
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.rating, 5)

    def test_review_unique_constraint(self):
        """Test that duplicate reviews raise a unique constraint error."""
        with self.assertRaises(ValidationError):
            duplicate_review = Review(
                user=self.user,
                product=self.product,
                rating=4,
                comment='Duplicate review'
            )
            duplicate_review.full_clean()  # Triggers unique constraint validation.

