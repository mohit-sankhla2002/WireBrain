from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ["id","username", "email", "phone", "is_admin", "profile_photo"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "username", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "phone", "profile_photo","team", "otp", "is_verified"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "username", "phone", "password1", "password2", "otp", "is_verified"],
            },
        ),
    ]
    search_fields = ["email", "username", "phone"]
    ordering = ["updated_at","email", "id"]
    filter_horizontal = []

admin.site.register(models.User, UserAdmin)