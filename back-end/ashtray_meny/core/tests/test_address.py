from django.test import TestCase
from ..models import Address, User
from django.core.exceptions import ValidationError

class AddressModelTests(TestCase):
    """Tests for the Address model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='addressuser@example.com',
            username='addressuser',
            password='Addressuser123!'
        )

    def test_create_address_successful(self):
        address = Address.objects.create(
            user=self.user,
            street='123 Main St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345'
        )
        self.assertEqual(address.street, '123 Main St')

    def test_create_address_without_street(self):
        with self.assertRaises(ValueError):
            Address.objects.create(
                user=self.user,
                street='',
                city='Test City',
                state='Test State',
                country='Test Country',
                postal_code='12345'
            )

    def test_create_address_without_city(self):
        with self.assertRaises(ValueError):
            Address.objects.create(
                user=self.user,
                street='123 Main St',
                city='',
                state='Test State',
                country='Test Country',
                postal_code='12345'
            )

    def test_create_address_without_postal_code(self):
        with self.assertRaises(ValueError):
            Address.objects.create(
                user=self.user,
                street='123 Main St',
                city='Test City',
                state='Test State',
                country='Test Country',
                postal_code=''
            )

    def test_address_created_at(self):
        address = Address.objects.create(
            user=self.user,
            street='456 Another St',
            city='Another City',
            state='Another State',
            country='Another Country',
            postal_code='67890'
        )
        self.assertIsNotNone(address.created_at)

    def test_address_update_postal_code(self):
        address = Address.objects.create(
            user=self.user,
            street='789 New St',
            city='New City',
            state='New State',
            country='New Country',
            postal_code='11111'
        )
        address.postal_code = '22222'
        address.save()
        self.assertEqual(address.postal_code, '22222')

    def test_address_validation(self):
        address = Address(
            user=self.user,
            street='',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345'
        )
        with self.assertRaises(ValidationError):
            address.full_clean()  # Triggers validation

    def test_address_retrieval_by_user(self):
        address = Address.objects.create(
            user=self.user,
            street='123 Main St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345'
        )
        retrieved_address = Address.objects.get(user=self.user)
        self.assertEqual(retrieved_address, address)

    def test_address_user_relation(self):
        address = Address.objects.create(
            user=self.user,
            street='123 Main St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345'
        )
        self.assertEqual(address.user.username, self.user.username)
