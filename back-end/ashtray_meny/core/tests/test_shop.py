from django.test import TestCase
from ..models import Shop
from django.contrib.auth import get_user_model

User = get_user_model()

class ShopModelTests(TestCase):
    """Tests for the Shop model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='shopowner@example.com',
            username='shopowner',
            password='Shopowner123!'
        )

    def test_create_shop_successful(self):
        shop = Shop.objects.create(
            shop_name='Test Shop',
            shop_owner=self.user,
            about_shop='A great shop.',
            how_old_is_the_shop=2
        )
        self.assertEqual(shop.shop_name, 'Test Shop')
        self.assertEqual(shop.shop_owner, self.user)

    def test_create_shop_without_name(self):
        with self.assertRaises(ValueError):
            Shop.objects.create(shop_name='', shop_owner=self.user)

    def test_shop_image_upload(self):
        shop = Shop.objects.create(
            shop_name='Shop with Image',
            shop_owner=self.user,
            shop_image='path/to/image.jpg',
        )
        self.assertEqual(shop.shop_image, 'path/to/image.jpg')

    def test_shop_verification_status(self):
        shop = Shop.objects.create(
            shop_name='Verified Shop',
            shop_owner=self.user,
            is_verified=True
        )
        self.assertTrue(shop.is_verified)

    def test_shop_views_default(self):
        shop = Shop.objects.create(
            shop_name='Shop with Default Views',
            shop_owner=self.user
        )
        self.assertEqual(shop.shop_views, 0)

    def test_shop_profit_this_month_default(self):
        shop = Shop.objects.create(
            shop_name='Shop with Default Profit',
            shop_owner=self.user
        )
        self.assertEqual(shop.profit_this_month, 0.00)

    def test_shop_active_default(self):
        shop = Shop.objects.create(
            shop_name='Active Shop',
            shop_owner=self.user
        )
        self.assertTrue(shop.is_active)

    def test_shop_about_description(self):
        shop = Shop.objects.create(
            shop_name='Descriptive Shop',
            shop_owner=self.user,
            about_shop='A shop with various products.'
        )
        self.assertEqual(shop.about_shop, 'A shop with various products.')

    def test_shop_created_at(self):
        shop = Shop.objects.create(
            shop_name='Timestamped Shop',
            shop_owner=self.user
        )
        self.assertIsNotNone(shop.shop_created_at)

    def test_shop_name_uniqueness(self):
        Shop.objects.create(
            shop_name='Unique Shop',
            shop_owner=self.user
        )
        with self.assertRaises(Exception):
            Shop.objects.create(
                shop_name='Unique Shop',
                shop_owner=self.user
            )
