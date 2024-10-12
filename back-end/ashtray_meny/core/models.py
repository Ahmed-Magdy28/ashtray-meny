# Import essential Django modules for model creation and validation.
from django.db import models  # Core Django ORM module to define models.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# AbstractBaseUser: For custom user models.
# PermissionsMixin: For handling user permissions.

from django.core.exceptions import ValidationError  # Raise validation errors.
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
# Validators: Ensure data constraints (e.g., minimum value, file type validation).

from django.utils import timezone  # Utility to manage date and time fields.
import uuid  # Module to generate unique UUID identifiers.

# Import custom validators (assumed to be defined in the project).
from core.validators import validate_image_size, validate_password_strength


# UserManager class handles user creation and management operations.
class UserManager(BaseUserManager):
    """Manager for User model, handling user creation and management."""

    def create_user(self, email, password, username, **extra_fields):
        """Creates a user with an email, password, and username."""
        if not email:
            raise ValueError("The email field is required.")  # Ensure email is provided.
        if not username:
            raise ValueError("The username field is required.")  # Ensure username is provided.

        validate_password_strength(password)  # Validate password strength using custom logic.
        email = self.normalize_email(email)  # Normalize email for consistency.

        # Create user with email, username, and extra fields.
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hash the password before saving.
        user.save(using=self._db)  # Save the user to the database.
        return user

    def create_superuser(self, email, username, password):
        """Creates a superuser with elevated privileges."""
        user = self.create_user(email=email, username=username, password=password)
        user.is_staff = True  # Set staff status to true.
        user.is_superuser = True  # Set superuser status to true.
        user.is_verified = True  # Mark as verified.
        user.save(using=self._db)  # Save superuser to the database.
        return user


# Custom User model extending Django's AbstractBaseUser.
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that allows authentication with email and adds extra fields.
    """

    # UUID field ensures unique identification for every user.
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    # Email is the primary identifier with uniqueness enforced.
    email = models.EmailField(max_length=255, unique=True)

    # Username with a database index for quick lookups.
    username = models.CharField(max_length=255, unique=True, db_index=True)

    # Boolean flags for account status and roles.
    is_active = models.BooleanField(default=True)  # Active status.
    is_staff = models.BooleanField(default=False)  # Staff user status.
    shop_owner = models.BooleanField(default=False)  # Indicates if the user owns a shop.
    is_verified = models.BooleanField(default=False)  # Indicates email verification status.

    # Optional profile image with size and file type validation.
    user_image = models.ImageField(
        upload_to='users/', blank=True, null=True,
        validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    # Optional age field with a minimum value of 1.
    user_age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])

    # JSON fields for wish list and address storage.
    wish_list = models.JSONField(default=list)
    address = models.JSONField(default=list)

    # Timestamp fields for creation date and last password update.
    created_in = models.DateTimeField(default=timezone.now)
    password_updated_at = models.DateTimeField(auto_now=True)

    # Track orders.
    orders_completed = models.IntegerField(default=0)  # Completed orders.
    orders_now = models.IntegerField(default=0)  # Current active orders.

    # Optional field for a personal description.
    about_user = models.TextField(blank=True, null=True)

    # Use UserManager to manage user creation.
    objects = UserManager()

    # Set email as the username field for authentication.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """String representation of the User instance."""
        return self.email  # Display the user's email address.


# Shop model representing a store.
class Shop(models.Model):
    """Model representing a shop owned by a user."""

    # UUID field for unique identification.
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    # Name of the shop with uniqueness constraint.
    shop_name = models.CharField(max_length=255, unique=True)

    # Foreign key linking the shop to its owner.
    shop_owner = models.ForeignKey(User, related_name='owned_shops', on_delete=models.CASCADE)

    # Images for the shop with validation.
    shop_image = models.ImageField(
        upload_to='shops/', blank=True, null=True,
        validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    shop_logo = models.ImageField(
        upload_to='shop_logos/', blank=True, null=True,
        validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    # JSON fields for colors, categories, and best-sellers.
    shop_identity_colors = models.JSONField(default=list, blank=True, null=True)
    shop_selling_categories = models.JSONField(default=list)
    best_sellers = models.JSONField(default=list)

    # Track shop views, sales, and profits.
    shop_views = models.PositiveIntegerField(default=0)
    monthly_sold_items = models.PositiveIntegerField(default=0)
    profit_this_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit_this_year = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Shop creation date.
    shop_created_at = models.DateTimeField(auto_now_add=True)

    # Optional description and status fields.
    about_shop = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Optional physical address field.
    shop_physical_address = models.CharField(max_length=255, blank=True, null=True)

    # Many-to-many field linking users who added items to the shop.
    shop_items_adders = models.ManyToManyField(User, related_name='added_items_shops', blank=True)

    def clean(self):
        """Validate that the shop identity colors are within the allowed limit."""
        if len(self.shop_identity_colors) > 3:
            raise ValidationError("shop_identity_colors can only contain a maximum of 3 colors.")

    def __str__(self):
        """String representation of the Shop instance."""
        return self.shop_name


# Product model representing individual products.
class Product(models.Model):
    """Model representing a product in a shop."""

    # Product status choices.
    class ProductStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    # UUID for unique product identification.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Product information fields.
    product_name = models.CharField(max_length=150)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField()

    # Price and quantity fields with validation.
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantity_available = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    # Dimensions and weight fields.
    dimensions = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])

    # Primary image with validation.
    image_1 = models.ImageField(
        upload_to='products/', validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    # Product status and timestamps.
    product_status = models.CharField(max_length=10, choices=ProductStatus.choices, default=ProductStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Foreign keys to the shop and category.
    shop = models.ForeignKey(Shop, related_name='shop_products', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='category_products', on_delete=models.CASCADE)

    def __str__(self):
        """String representation of the Product instance."""
        return self.product_name


