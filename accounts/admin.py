from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields shown in the user list
    list_display = (
        "id", "email", "username", "first_name", "last_name",
        "mobile_no", "address", "pin_code", "is_staff", "is_active"
    )
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Make username read-only
    readonly_fields = ("username", "created_at", "updated_at")

    # Field layout for editing existing users
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "mobile_no", "address", "pin_code")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login", "created_at", "updated_at")
        }),
    )

    # Fields used when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "mobile_no", "address", "pin_code", "password1", "password2"),
        }),
    )

    search_fields = ("email", "username", "mobile_no", "first_name", "last_name")
    ordering = ("-created_at",)

    # Show username in the header (object display)
    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        if obj:
            obj._meta.verbose_name = f"User: {obj.username}"
        return obj
