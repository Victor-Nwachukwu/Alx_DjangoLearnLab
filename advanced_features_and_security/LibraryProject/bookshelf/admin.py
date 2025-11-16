
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for CustomUser
    """

    model = CustomUser

    # Fields for display in change list (Admin)
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_active")

    # Fields editable in admin user form
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
        )}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields used when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "date_of_birth", "profile_photo", "is_staff", "is_active")
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
