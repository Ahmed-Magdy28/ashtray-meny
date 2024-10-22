from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.contrib.auth import get_user_model
from core.validators import validate_image_size, validate_password_strength




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


class ShopManager(models.Manager):
    def create_shop(self, shop_name, user, **extra_fields):
        """
        Create a new shop and set the user as the shop owner.

        Args:
            shop_name (str): The name of the new shop.
            user (User): The user who will own the shop.
            **extra_fields: Additional fields to set on the shop.

        Returns:
            Shop: The created shop instance.
        """
        if not shop_name:
            raise ValueError("The shop must have a unique name.")
        if user.shop_owner:
            raise ValueError("This user already owns a shop.")

        with transaction.atomic():
            # Create shop
            shop = self.model(shop_name=shop_name, shop_owner=user, **extra_fields)
            shop.save(using=self._db)

            # Update user to be a shop owner
            user.shop_owner = True
            user.save(update_fields=['shop_owner'])

        return shop


class CategoryManager(models.Manager):
    """Custom manager for Category model to handle category-specific queries."""

    def create_category(self, name, description=None, category_image=None):
        """Method to create a category with validation."""
        if not name:
            raise ValueError('Category must have a name')
        category = self.create(name=name, description=description, category_image=category_image)
        return category

    def with_products(self):
        """Returns categories that have products."""
        return self.filter(products__isnull=False).distinct()


class ProductManager(models.Manager):
    """Custom manager for the Product model to handle product-specific queries."""

    def create_product(self, user, shop_id, product_name, price, quantity_available, category, **extra_fields):
        """
        Create a new product for a shop.

        Args:
            user (User): The user creating the product. They must own the shop.
            shop_id (UUID): The ID of the shop where the product is being created.
            product_name (str): The name of the product.
            price (Decimal): The price of the product.
            quantity_available (int): Available stock for the product.
            **extra_fields: Additional fields to set on the product.

        Returns:
            Product: The created product instance.

        Raises:
            ValidationError: If the user doesn't own the shop or required fields are missing.
        """
        shop = Shop.objects.filter(unique_id=shop_id, shop_owner=user).first()
        if not shop:
            raise ValidationError("You do not own this shop or the shop does not exist.")

        # Validate product creation details
        if not product_name or price <= 0 or quantity_available < 0:
            raise ValidationError("Invalid product details.")

        with transaction.atomic():
            product = self.model(
                shop=shop,
                product_name=product_name,
                price=price,
                quantity_available=quantity_available,
                category=category,
                **extra_fields
            )
            product.save(using=self._db)

        return product


# Review Manager
class ReviewManager(models.Manager):
    def create_review(self, user, product=None, shop=None, rating=1, comment=""):
        if not (product or shop):
            raise ValidationError("A review must be linked to a product or a shop.")
        return self.create(user=user, product=product, shop=shop, rating=rating, comment=comment)

# Order Manager
class OrderManager(models.Manager):
    def create_order(self, user, total_amount, products=None, status='pending'):
        order = self.model(user=user, total_amount=total_amount, order_status=status)
        order.save(using=self._db)
        if products:
            order.products.set(products)
        return order

# Address Manager
class AddressManager(models.Manager):
    def create_address(self, user, street, city, postal_code, country):
        return self.create(user=user, street=street, city=city, postal_code=postal_code, country=country)

class Shop(models.Model):
    """
    Model representing a shop.

    Attributes:
        name (str): The name of the shop.
        shop_identity_colors (list): A list of up to 3 colors representing the shop's identity.
        shop_physical_address (str): The physical location of the shop.
        shop_items_adders (ManyToManyField): Users who have added items to the shop.
    """
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    shop_name = models.CharField(max_length=255, unique=True)
    shop_owner = models.ForeignKey('User', related_name='owned_shops', on_delete=models.CASCADE)
    shop_image = models.ImageField(upload_to='shops/', blank=True, null=True,
                                   validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    shop_background_image = models.ImageField(upload_to='shop_backgrounds/', blank=True, null=True,
                                              validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    category = models.ManyToManyField('Category', related_name='shop_categories', blank=True)
    best_sellers = models.ManyToManyField('Product', related_name='shop_best_sellers', blank=True)
    shop_views = models.IntegerField(default=0)
    shop_reviews_is_on = models.BooleanField(default=True)
    monthly_sold_items = models.IntegerField(default=0)
    sales_this_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shop_created_at = models.DateTimeField(auto_now_add=True)
    about_shop = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = ShopManager()


    def __str__(self):
        return self.shop_name  # Return the name of the shop for representation.

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model extending AbstractUser with additional fields.
    """
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    shop_owner = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    user_image = models.ImageField(upload_to='users/', blank=True, null=True,
                                   validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    user_age = models.IntegerField(null=True, blank=True)
    default_address = models.ForeignKey('Address', related_name='default_user', on_delete=models.SET_NULL, null=True, blank=True)
    created_in = models.DateTimeField(default=timezone.now)
    orders_completed = models.IntegerField(default=0)
    orders_now = models.IntegerField(default=0)
    password_updated_at = models.DateTimeField(auto_now=True)
    about_user = models.TextField(blank=True, null=True)

    # New fields
    user_country = models.CharField(max_length=100, blank=True, null=True)  # Country as string
    user_shop = models.OneToOneField(Shop, null=True, blank=True, on_delete=models.SET_NULL)  # One-to-one relationship with Shop

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email  # Return email address for user representation.




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

    objects = ProductManager()

    def __str__(self):
        """String representation of the Product instance, returning the product name."""
        return self.product_name

class Category(models.Model):
    """Category model representing product categories."""
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)  # Unique identifier for the category
    name = models.CharField(max_length=255, unique=True)  # Unique name for the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category
    products = models.ManyToManyField('Product', related_name='categories', blank=True)  # List of products in this category
    category_image = models.ImageField(upload_to='category_images/', blank=True, null=True, validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # Image associated with the category

    def __str__(self):
        return self.name  # String representation of the category

    objects = CategoryManager()

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
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, blank=True, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

    objects = AddressManager()

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
        ratings = self.ratings.all()  # Make sure to access ratings correctly

    def __str__(self):
        product_name = self.product.product_name if self.product else "No Product"
        shop_name = self.shop.shop_name if self.shop else "No Shop"
        return f'Review by {self.user.username} for {product_name} or {shop_name}'


    objects = ReviewManager()

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
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        SHIPPED = 'shipped', 'Shipped'
        CANCELLED = 'cancelled', 'Cancelled'

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders', blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.unique_id} by {self.user.username}"


    objects = OrderManager()

class WishList(models.Model):
    user = models.ForeignKey(User, related_name='wishlists', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlisted_by', on_delete=models.CASCADE)
