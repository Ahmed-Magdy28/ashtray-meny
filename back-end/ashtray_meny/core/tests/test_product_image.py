from django.test import TestCase
from ..models import Product, ProductImage, Shop
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductImageModelTests(TestCase):
    """Tests for the ProductImage model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='imageowner@example.com',
            username='imageowner',
            password='Imageowner123!'
        )
        self.shop = Shop.objects.create(
            shop_name='Image Shop',
            shop_owner=self.user
        )
        self.product = Product.objects.create(
            product_name='Image Product',
            shop=self.shop,
            short_description='desc',
            long_description='long desc',
            category='cat'
        )

    def test_create_product_image_successful(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg'
        )
        self.assertEqual(image.product, self.product)

    def test_create_product_image_without_product(self):
        with self.assertRaises(ValueError):
            ProductImage.objects.create(product=None, image='path/to/image.jpg')

    def test_create_product_image_without_image(self):
        with self.assertRaises(ValueError):
            ProductImage.objects.create(product=self.product, image='')

    def test_product_image_upload(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg'
        )
        self.assertEqual(image.image, 'path/to/image.jpg')

    def test_product_image_default_order(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg',
            order=1
        )
        self.assertEqual(image.order, 1)

    def test_product_image_multiple_uploads(self):
        image1 = ProductImage.objects.create(
            product=self.product,
            image='path/to/image1.jpg'
        )
        image2 = ProductImage.objects.create(
            product=self.product,
            image='path/to/image2.jpg'
        )
        self.assertNotEqual(image1.pk, image2.pk)

    def test_product_image_format_validation(self):
        with self.assertRaises(ValueError):
            ProductImage.objects.create(
                product=self.product,
                image='invalid_format.txt'
            )

    def test_product_image_product_relation(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg'
        )
        self.assertEqual(image.product.shop, self.shop)

    def test_product_image_created_at(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg'
        )
        self.assertIsNotNone(image.created_at)

    def test_product_image_update_image(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg'
        )
        image.image = 'path/to/updated_image.jpg'
        image.save()
        self.assertEqual(image.image, 'path/to/updated_image.jpg')
