from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.contrib.auth import get_user_model
from validators import validate_image_size, validate_password_strength




class UserManager(BaseUserManager):
    """Manager for User model, handling user creation and management."""

    def create_user(self, email, password, username, **extra_fields):
        """
        Creates and returns a user with an email and password.

        Args:
            email (str): The email address for the user.
            password (str): The password for the user.
            **extra_fields: Additional fields to set on the user.

        Returns:
            User: The created user instance.
        """
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a unique username.")

        validate_password_strength(password)

        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save the user to the database
        return user # Return the created user.

    def create_superuser(self, email, username, password):
        """
        Creates and returns a superuser with an email and password.

        Args:
            email (str): The email address for the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields to set on the superuser.

        Returns:
            User: The created superuser instance.
        """
        user = self.create_user(email=email, username=username, password=password)
        user.is_staff = True  # Grant staff status
        user.is_superuser = True  # Grant superuser status
        user.is_verified = True  # Consider adding this
        user.save(using=self._db)  # Save the superuser to the database
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model extending AbstractUser with additional fields.

    This model allows for user accounts with an email address as the username
    and includes an optional personal description field.
    """
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)  # Unique identifier.
    email = models.EmailField(max_length=255, unique=True)  # Email field with uniqueness constraint.
    username = models.CharField(max_length=255, unique=True, db_index=True)  # Unique username field with index.
    is_active = models.BooleanField(default=True)  # Boolean field for active status.
    is_staff = models.BooleanField(default=False)  # Boolean field for staff status.
    shop_owner = models.BooleanField(default=False)  # Boolean field indicating shop ownership.
    is_verified = models.BooleanField(default=False)  # Boolean field for verification status.
    user_image = models.ImageField(upload_to='users/', blank=True, null=True,  # Field for user profile image.
                                    validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # Validator for image file types.
    user_age = models.IntegerField(null=True, blank=True)  # Optional field for user age.
    wish_list = models.JSONField(default=list)  # JSON field for storing user wishlist items.
    default_address = models.CharField(max_length=255, blank=True, null=True, help_text="Optional field for default user address")  # Optional field for default user address.
    addresses = models.JSONField(default=list)  # JSON field for storing user addresses.
    created_in = models.DateTimeField(default=timezone.now)  # Timestamp for when the user was created.
    orders_completed = models.IntegerField(default=0)  # Field for completed orders count.
    orders_now = models.IntegerField(default=0)  # Field for current orders count.
    password_updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last password update.
    about_user = models.TextField(blank=True, null=True, help_text="A personal description of the user.") # Optional text field for user description.

    objects = UserManager()  # Assign UserManager for user operations.

    USERNAME_FIELD = 'email'  # Specify email as the username field.
    REQUIRED_FIELDS = ['username']  # Specify required fields for creating a user.


    def __str__(self):
        return self.email  # Return email address for user representation.


class Shop(models.Model):
    """
    Model representing a shop.

    Attributes:
        name (str): The name of the shop.
        shop_identity_colors (list): A list of up to 3 colors representing the shop's identity.
        shop_physical_address (str): The physical location of the shop.
        shop_items_adders (ManyToManyField): Users who have added items to the shop.
    """
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)  # Unique identifier.
    shop_name = models.CharField(max_length=255, unique=True)  # Unique shop name.
    shop_owner = models.ForeignKey(User, related_name='owned_shops', on_delete=models.CASCADE)  # Foreign key to the User model.
    shop_image = models.ImageField(upload_to='shops/', blank=True, null=True,  # Field for shop image.
                                    validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # Validator for image file types.
    shop_background_image = models.ImageField(upload_to='shop_backgrounds/', blank=True, null=True,  # Field for shop background image.
                                               validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # Validator for image file types.
    shop_identity_colors = models.JSONField(default=list, blank=True, null=True, help_text="A list of up to 3 colors representing the shop's identity.")  # JSON field for shop identity colors.
    shop_selling_categories = models.JSONField(default=list)  # JSON field for categories the shop sells.
    best_sellers = models.JSONField(default=list)  # JSON field for best-selling products.
    shop_views = models.IntegerField(default=0)  # Field for tracking shop views.
    shop_reviews_is_on = models.BooleanField(default=True)  # Boolean field indicating if reviews are allowed.
    monthly_sold_items = models.IntegerField(default=0)  # Field for tracking items sold this month.
    sales_this_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Decimal field for current month's profit.
    sales_last_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Decimal field for last month's profit.
    sales_this_year = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Decimal field for current year's profit.
    shop_created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the shop was created.
    about_shop = models.TextField(blank=True, null=True)  # Optional text field for shop description.
    how_old_is_the_shop = models.IntegerField(default=0)  # Field for tracking the age of the shop.
    is_verified = models.BooleanField(default=False)  # Boolean field for shop verification status.
    is_active = models.BooleanField(default=True)  # Boolean field indicating if the shop is active.
    # shop_product_adders = models.ManyToManyField(User, related_name='added_items_shops', blank=True, help_text="Users who have added items to the shop.")  # Many-to-many relationship with users who added items to the shop.
    # shop_analytics_viewers = models.ManyToManyField(User, related_name='viewed_shop_analytics', blank=True, help_text="Users who have viewed shop analytics.")  # Many-to-many relationship with users who viewed shop analytics.

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure that shop_identity_colors contains
        a maximum of 3 colors.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        if isinstance(self.shop_identity_colors, list) and len(self.shop_identity_colors) > 3:
            raise ValueError("shop_identity_colors can only contain a maximum of 3 colors.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop_name  # Return the name of the shop for representation.




class Product(models.Model):
    """
    Model representing a product.

    Attributes:
        name (str): The name of the product.
        description (str): A brief description of the product.
        price (Decimal): The price of the product.
        dimensions (str): The dimensions of the product (length x width x height).
        quantity_available (int): The amount of this product currently in stock (inventory tracking).
        product_status (str): The current status of the product (e.g., active, inactive).
    """
    class ProductStatus(models.TextChoices):
        """Defines the possible statuses for a product."""
        ACTIVE = 'active', 'Active'  # Indicates that the product is currently available for purchase.
        INACTIVE = 'inactive', 'Inactive'  # Indicates that the product is currently not available for purchase.

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """Unique identifier for the product, automatically generated as a UUID."""

    product_name = models.CharField(max_length=150, help_text='Enter the product name.')
    """Name of the product with a maximum length of 150 characters."""

    short_description = models.CharField(max_length=300, help_text='Enter a short description of the product.')
    """Brief description of the product, limited to 300 characters."""

    long_description = models.TextField(help_text='Enter a long description of the product.')
    """Detailed description of the product, allowing for larger amounts of text."""

    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0.01)],
                                error_messages={'min_value': 'Price must be greater than zero.'})
    """Price of the product with up to 10 digits and 2 decimal places, must be greater than zero."""

    quantity_available = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        error_messages={'min_value': 'Quantity must be zero or more.'}
    )
    """Available stock quantity for the product, must be a non-negative integer."""

    how_many_sold = models.PositiveIntegerField(default=0)
    """Tracks the total number of units sold, defaulting to 0."""

    how_many_views = models.PositiveIntegerField(default=0)
    """Counts the number of times the product has been viewed, defaulting to 0."""

    dimensions = models.CharField(max_length=50, help_text='Enter the dimensions of the product (e.g., 10x10x10 cm).')
    """Dimensions of the product, represented as a string, with a maximum length of 50 characters."""

    weight = models.DecimalField(max_digits=5, decimal_places=2,
                                 validators=[MinValueValidator(0.01)],
                                 error_messages={'min_value': 'Weight must be greater than zero.'})
    """Weight of the product with up to 5 digits and 2 decimal places, must be greater than zero."""

    image_1 = models.ImageField(upload_to='products/', validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], help_text='Upload the primary product image.')
    """Primary image of the product, uploaded to the 'products/' directory, validated for the correct image format."""

    image_2 = models.ImageField(upload_to='products/', blank=True, null=True, validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], help_text='Upload a secondary product image (optional).')
    """Secondary image of the product, optional field, uploaded to the 'products/' directory, validated for the correct image format."""

    image_3 = models.ImageField(upload_to='products/', blank=True, null=True, validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], help_text='Upload a third product image (optional).')
    """Tertiary image of the product, optional field, uploaded to the 'products/' directory, validated for the correct image format."""

    product_status = models.CharField(max_length=10, choices=ProductStatus.choices, default=ProductStatus.ACTIVE)
    """Current status of the product, selected from predefined choices, defaults to 'Active'."""

    created_at = models.DateTimeField(auto_now_add=True)
    """Timestamp indicating when the product was created, automatically set on creation."""

    updated_at = models.DateTimeField(auto_now=True)
    """Timestamp indicating when the product was last updated, automatically set on every save."""

    # ForeignKey examples (assuming you have Shop and Category models)
    shop = models.ForeignKey('Shop', related_name='shop_products', on_delete=models.CASCADE)
    """Reference to the Shop model, indicating the shop that sells this product; deletes related products on shop deletion."""

    category = models.ForeignKey('Category', related_name='category_products', on_delete=models.CASCADE)
    """Reference to the Category model, indicating the category to which this product belongs; deletes related products on category deletion."""

    def __str__(self):
        """String representation of the Product instance, returning the product name."""
        return self.product_name



class PriceHistory(models.Model):
    """Model to keep track of product price changes."""
    product = models.ForeignKey(Product, related_name='price_history', on_delete=models.CASCADE)  # Foreign key linking to the Product model.
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])  # Field for recorded price.
    changed_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the price was changed.

    def __str__(self):
        return f'Price history for {self.product.product_name} at {self.changed_at}'  # Return a descriptive string for the price history.


class ProductImage(models.Model):
    """Model for storing multiple images for a product."""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    def __str__(self):
        return f'Image for {self.product.product_name}'  # Return a descriptive string for the image.

class Address(models.Model):
    """Address model for storing user and shop addresses."""
    user = models.ForeignKey(User, related_name='addresses',
                             on_delete=models.CASCADE, blank=True, null=True)
    shop = models.ForeignKey(Shop, related_name='addresses',
                             on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address



class Review(models.Model):
    """Model for storing reviews for products and shops."""
    user = models.ForeignKey(User, related_name='reviews',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews',
                                on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey(Shop, related_name='reviews',
                             on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                      MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_images = models.JSONField(default=list, blank=True)  # Store
    # URLs or file paths of images
    class Meta:
        unique_together = ('user', 'product', 'shop')

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.rating_value for rating in ratings) / ratings.count()
        return 0

    def __str__(self):
        product_name = self.product.product_name if self.product else "No Product"
        shop_name = self.shop.shop_name if self.shop else "No Shop"
        return f'Review by {self.user.username} for {product_name} or {shop_name}'

class ReviewRating(models.Model):
    review = models.ForeignKey(Review, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating_value = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['review', 'user'], name='unique_review_rating')
        ] # A user can only rate a review once

    def clean(self):
        if self.rating_value < 1 or self.rating_value > 5:
            raise ValidationError('Rating value must be between 1 and 5.')




class Order(models.Model):
    """Model for storing orders made by users."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)  # Unique identifier for the order
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)  # User who made the order
    products = models.ManyToManyField(Product, related_name='orders', blank=True)  # List of products in the order
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount for the order
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')  # Current status of the order (e.g., pending, completed)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the order was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the order was last updated

    def __str__(self):
        return f"Order {self.unique_id} by {self.user.username}"


class Category(models.Model):
    """Category model representing product categories."""
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)  # Unique identifier for the category
    name = models.CharField(max_length=255, unique=True)  # Unique name for the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category
    products = models.ManyToManyField('Product', related_name='categories', blank=True)  # List of products in this category
    category_image = models.ImageField(upload_to='category_images/', blank=True, null=True, validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # Image associated with the category

    def __str__(self):
        return self.name  # String representation of the category



class WishList(models.Model):
    user = models.ForeignKey(User, related_name='wishlists', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlisted_by', on_delete=models.CASCADE)
