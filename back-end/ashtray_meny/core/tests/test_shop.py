from django.test import TestCase
from core.models import User, Shop

class ShopModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='Password123!', username='testuser')

    def test_create_shop(self):
        # Ensure user is not a shop owner initially
        self.assertFalse(self.user.shop_owner)

        # Create a shop for the user
        shop = Shop.objects.create_shop(shop_name='Test Shop', user=self.user)

        # Check that the shop was created
        self.assertEqual(Shop.objects.count(), 1)
        self.assertEqual(shop.shop_name, 'Test Shop')

        # Ensure the user is now a shop owner
        self.user.refresh_from_db()
        self.assertTrue(self.user.shop_owner)

        # Ensure the user cannot create another shop
        with self.assertRaises(ValueError):
            Shop.objects.create_shop(shop_name='Another Shop', user=self.user)
