from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations Personnelles", {"fields": ("first_name", "last_name")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Dates Importantes", {"fields": ("last_login", "date_joined")}),
        ("Rôle", {"fields": ("role",)}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "role"),
        }),
    )
    
    list_display = ["email", "role", "is_active", "is_staff"]
    ordering = ['email']
    list_filter = ["role", "is_active", "is_staff"]
    search_fields = ["email"]