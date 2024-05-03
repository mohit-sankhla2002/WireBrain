from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ["id","username", "email", "phone", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "username", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "phone"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "username", "phone", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "username", "phone"]
    ordering = ["updated_at","email", "id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)