"""Django admin Customization"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models

class UserAdmin(BaseUserAdmin):
    """Define the Admin Pages For Users."""
    ordering = ['username']
    list_display = ['email', 'username', 'is_active', 'is_verified', 'shop_owner', 'created_in']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Profile'), {'fields': ('user_image', 'user_age', 'about_user')}),
        (_('Orders'), {'fields': ('orders_completed', 'orders_now')}),
        (
            _('Permissions'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'shop_owner',
                    'is_verified',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'password_updated_at', 'created_in')}),
    )

    readonly_fields = ['last_login', 'password_updated_at', 'created_in']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',
                       'is_active', 'is_staff', 'is_superuser', 'shop_owner', 'is_verified'),
        }),
    )


# Register the User model with the customized UserAdmin
admin.site.register(models.User, UserAdmin)


# Registering the rest of the models
@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'shop_owner', 'is_active', 'is_verified']
    search_fields = ['shop_name', 'shop_owner__username']
    list_filter = ['is_active', 'is_verified']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'shop', 'price', 'quantity_available', 'product_status']
    search_fields = ['product_name', 'shop__shop_name']
    list_filter = ['product_status', 'shop']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'user', 'order_status', 'total_amount']
    search_fields = ['user__email', 'unique_id']
    list_filter = ['order_status']


@admin.register(models.WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'shop', 'rating', 'created_at']
    search_fields = ['user__email', 'product__product_name', 'shop__shop_name']
    list_filter = ['rating']


@admin.register(models.ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'rating_value']


@admin.register(models.PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'changed_at']


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street', 'city', 'country']
