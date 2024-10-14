from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import Category, Product, User, Shop  # Import User and Shop

class CategoryManagerTest(TestCase):

    def setUp(self):
        """Set up test data."""
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Fashion")

        # Create a user and a shop for the product creation
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="OwnerPass123!",
            username="shop_owner"
        )
        self.shop = Shop.objects.create(shop_name="My Awesome Shop", shop_owner=self.user)

    def test_create_category(self):
        """Test the creation of a category with the custom manager."""
        category = Category.objects.create_category(name="Books", category_image=None)
        self.assertEqual(category.name, "Books")
        self.assertIsNone(category.description)
        self.assertEqual(category.category_image.name, None)

    def test_create_category_without_name(self):
        """Test that creating a category without a name raises an error."""
        with self.assertRaises(ValueError):
            Category.objects.create_category(name="")

    def test_with_products(self):
        """Test the manager method that returns categories with products."""
        product = Product.objects.create_product(
            user=self.user,
            shop_id=self.shop.unique_id,
            product_name="Laptop",
            short_description="A cool laptop",
            long_description="A powerful laptop with excellent features.",
            price=1000,
            quantity_available=10,
            dimensions="15x10x0.7 inches",
            weight=3.5,
            category=self.category1
        )
        self.category1.products.add(product)

        categories_with_products = Category.objects.with_products()
        self.assertIn(self.category1, categories_with_products)
        self.assertNotIn(self.category2, categories_with_products)
