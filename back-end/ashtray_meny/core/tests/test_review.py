from django.test import TestCase
from ..models import Review, User, Product, Shop

class ReviewModelTests(TestCase):
    """Tests for the Review model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='reviewuser@example.com',
            username='reviewuser',
            password='Reviewuser123!'
        )
        self.shop = Shop.objects.create(
            shop_name='Review Shop',
            shop_owner=self.user
        )
        self.product = Product.objects.create(
            product_name='Review Product',
            shop=self.shop,
            short_description='desc',
            long_description='long desc',
            category='cat'
        )

    def test_create_review_successful(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            comment='Good product!',
            review_images='path/to/review_image.jpg'
        )
        self.assertEqual(review.rating, 4)

    def test_create_review_without_rating(self):
        with self.assertRaises(ValueError):
            Review.objects.create(
                user=self.user,
                product=self.product,
                rating=None,
                comment='No rating!',
                review_images='path/to/review_image.jpg'
            )

    def test_create_review_without_comment(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='',
            review_images='path/to/review_image.jpg'
        )
        self.assertEqual(review.comment, '')

    def test_review_image_upload(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            comment='Average product.',
            review_images='path/to/review_image.jpg'
        )
        self.assertEqual(review.review_images, 'path/to/review_image.jpg')

    def test_review_created_at(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Excellent!',
        )
        self.assertIsNotNone(review.created_at)

    def test_review_update_comment(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=2,
            comment='Not good.',
        )
        review.comment = 'Changed my mind.'
        review.save()
        self.assertEqual(review.comment, 'Changed my mind.')

    def test_review_user_relation(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            comment='Good product!',
        )
        self.assertEqual(review.user.username, self.user.username)

    def test_review_product_relation(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Amazing product!',
        )
        self.assertEqual(review.product.product_name, self.product.product_name)

    def test_review_rating_boundaries(self):
        with self.assertRaises(ValueError):
            Review.objects.create(
                user=self.user,
                product=self.product,
                rating=6,
                comment='Invalid rating!',
            )

    def test_review_retrieval_by_product(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Great product!',
        )
        retrieved_reviews = Review.objects.filter(product=self.product)
        self.assertIn(review, retrieved_reviews)
