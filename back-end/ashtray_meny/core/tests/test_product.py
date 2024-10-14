from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Shop, Product, User, Category # Import User and Category

class ProductManagerTest(TestCase):

    def setUp(self):
        # Create user, shop, and category for tests
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="OwnerPass123!",
            username="shop_owner"
        )
        self.shop = Shop.objects.create(shop_name="My Awesome Shop", shop_owner=self.user)
        self.category = Category.objects.create(name="Electronics")  # Create category

    def test_create_product_success(self):
        # Test successful product creation
        product = Product.objects.create_product(
            user=self.user,
            shop_id=self.shop.unique_id,
            product_name="Laptop",
            short_description="A cool laptop",
            long_description="A powerful laptop with excellent features.",
            price=9.99,
            quantity_available=10,
            dimensions="10x10x10 cm",
            weight=1.5,
            category=self.category  # Include category
        )
        self.assertIsNotNone(product)
        self.assertEqual(product.shop, self.shop)
        self.assertEqual(product.product_name, "Laptop")

    def test_create_product_invalid_shop(self):
        # Test creating a product for a shop the user doesn't own
        other_user = User.objects.create_user(
            email="other@example.com",
            password="OtherPass123!",
            username="not_owner"
        )
        with self.assertRaises(ValidationError):
            Product.objects.create_product(
                user=other_user,
                shop_id=self.shop.unique_id,
                product_name="Invalid Product",
                price=9.99,
                quantity_available=5,
                category=self.category  # Include category
            )

    def test_create_product_invalid_details(self):
        # Test creating a product with invalid details
        with self.assertRaises(ValidationError):
            Product.objects.create_product(
                user=self.user,
                shop_id=self.shop.unique_id,
                product_name="",
                price=-5,
                quantity_available=-1,
                category=self.category  # Include category
            )
