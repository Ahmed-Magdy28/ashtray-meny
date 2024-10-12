from django.test import TestCase
from ..models import Product, Shop
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductModelTests(TestCase):
    """Tests for the Product model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='productowner@example.com',
            username='productowner',
            password='Productowner123!'
        )
        self.shop = Shop.objects.create(
            shop_name='Shop for Products',
            shop_owner=self.user
        )

    def test_create_product_successful(self):
        product = Product.objects.create(
            product_name='Test Product',
            shop=self.shop,
            short_description='Short desc',
            long_description='Long description of the product.',
            category='Electronics',
            price_history=[{'price': 100.00, 'date': '2024-01-01'}]
        )
        self.assertEqual(product.product_name, 'Test Product')

    def test_create_product_without_name(self):
        with self.assertRaises(ValueError):
            Product.objects.create(product_name='', shop=self.shop, short_description='desc', long_description='long desc', category='cat')

    def test_create_product_with_invalid_price_history(self):
        with self.assertRaises(ValueError):
            Product.objects.create(
                product_name='Invalid Price Product',
                shop=self.shop,
                short_description='desc',
                long_description='long desc',
                category='cat',
                price_history='Invalid history'
            )

    def test_product_discount_default(self):
        product = Product.objects.create(
            product_name='Discount Product',
            shop=self.shop,
            short_description='desc',
            long_description='long desc',
            category='cat'
        )
        self.assertEqual(product.discount, 0.00)

    def test_product_views_default(self):
        product = Product.objects.create(
            product_name='Viewable Product',
            shop=self.shop,
            short_description='desc',
            long_description='long desc',
            category='cat'
        )
        self.assertEqual(product.how_many_views, 0)

    def test_product_sold_count_default(self):
        product = Product.objects.create(
            product_name='Sold Count Product',
            shop=self.shop,
            short_description='desc',
            long_description='long desc',
            category='cat'
        )
        self.assertEqual(product.how_many_sold, 0)

    def test_product_warranty_optional(self):
        product = Product.objects.create(
            product_name='Product with Warranty',
            shop=self.shop,
            short_description='desc',
            long_description='long desc',
            category='cat',
            warranty='2 years'
        )
        self.assertEqual(product.warranty, '2 years')

    def test_product_image_upload(self):
        product = Product.objects.create(
            product_name='Image Product',
            shop=self.shop,
            short_description='desc',
            long_description='long desc',
            category='cat',
            product_image='path/to/image.jpg'
        )
        self.assertEqual(product.product_image, 'path/to/image.jpg')

    def test_product_category_non_blank(self):
        with self.assertRaises(ValueError):
            Product.objects.create(
                product_name='Product without Category',
                shop=self.shop,
                short_description='desc',
                long_description='long desc',
                category=''
            )
