"""Django admin Customization"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define the Admin Pages For Users"""
    ordering = ['id']
    list_display = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (
            _('permissions'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields':
                                ('last_login',)
                                }),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2',
                           'is_active', 'is_staff', 'is_superuser')}),
    )


admin.site.register(models.User, UserAdmin)