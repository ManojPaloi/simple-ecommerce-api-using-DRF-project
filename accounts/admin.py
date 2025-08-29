from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser model"""

    model = CustomUser

    # Fields shown in the list view
    list_display = (
        "id", "email", "username", "first_name", "last_name",
        "mobile_no", "is_staff", "is_active", "created_at"
    )
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Read-only fields (auto-managed)
    readonly_fields = ("username", "created_at", "updated_at")

    # Layout for editing an existing user
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Information", {
            "fields": ("first_name", "last_name", "mobile_no", "address", "pin_code")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login", "created_at", "updated_at")
        }),
    )

    # Layout for creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "mobile_no",
                "address", "pin_code", "password1", "password2"
            ),
        }),
    )

    # Search and ordering
    search_fields = ("email", "username", "mobile_no", "first_name", "last_name")
    ordering = ("-created_at",)

    def get_object(self, request, object_id, from_field=None):
        """Show custom header in admin detail view"""
        obj = super().get_object(request, object_id, from_field)
        if obj:
            obj._meta.verbose_name = f"User: {obj.username}"
        return obj
