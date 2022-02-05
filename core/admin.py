from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        ('Main Head', {'fields': ('email', 'password')}),
        ('personal info', {'fields': ('name',)}),
        (
            'permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        ('important dates', {'fields': ('last_login',)})
    )

    add_fieldsets = (
        ('Add page', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
