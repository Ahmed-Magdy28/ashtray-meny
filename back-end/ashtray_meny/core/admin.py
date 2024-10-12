"""Django admin Customization"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define the Admin Pages For Users."""
    ordering = ['username']  # Ensure that the user list is ordered by the username
    list_display = ['email', 'username']  # Fields displayed in the user list
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),  # Fields to display in the user edit form
        (
            _('Permissions'), {
                'fields': (
                    'is_active',  # Indicates if the user is active
                    'is_staff',   # Indicates if the user has staff privileges
                    'is_superuser',  # Indicates if the user has superuser privileges
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),  # Display last login date
    )
    readonly_fields = ['last_login']  # Make last_login field read-only
    add_fieldsets = (
        (None, {'classes': ('wide',),  # Use a wide layout for the add user form
                'fields': ('username', 'email', 'password1', 'password2',
                           'is_active', 'is_staff', 'is_superuser')}),  # Fields for adding a new user
    )


# Register the User model with the customized UserAdmin
admin.site.register(models.User, UserAdmin)
