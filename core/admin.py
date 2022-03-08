from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models

from typing import Any,List, Tuple 

class UserAdmin(BaseUserAdmin):
    ordering: List[str] = ['id']
    list_display: List[str] = ['email', 'name']


    # Defining Any tuple, because here we don't have
    # any defined structure of code. 
    fieldsets: Tuple[Any] = (
        ('Main Head', {'fields': ('email', 'password')}),
        ('personal info', {'fields': ('name',)}),
        (
            'permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        ('important dates', {'fields': ('last_login',)})
    )

    add_fieldsets: Tuple[Any] = (
        ('Add page', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
