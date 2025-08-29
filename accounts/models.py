import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# -------------------------------------------------------------------
# Utilities
# -------------------------------------------------------------------

def generate_random_username(first_name: str = None) -> str:
    """
    Generate a unique username using the first name (if provided) + random suffix.
    Example: john_ab12cd
    """
    base = (first_name.lower() if first_name else "user")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{base}_{random_str}"


# -------------------------------------------------------------------
# User Manager
# -------------------------------------------------------------------

class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model with email as the unique identifier."""

    def create_user(self, email, password=None, first_name=None, mobile_no=None, **extra_fields):
        """Create and return a regular user with a unique username."""
        if not email:
            raise ValueError("The Email field is required.")

        email = self.normalize_email(email)

        # Generate unique username if not provided
        if not extra_fields.get("username"):
            proposed_username = generate_random_username(first_name)
            while CustomUser.objects.filter(username=proposed_username).exists():
                proposed_username = generate_random_username(first_name)
            extra_fields["username"] = proposed_username

        user = self.model(
            email=email,
            first_name=first_name or "",
            mobile_no=mobile_no,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with admin permissions."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password=password, **extra_fields)


# -------------------------------------------------------------------
# User Model
# -------------------------------------------------------------------

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model where email is the unique identifier."""

    # Identity
    username   = models.CharField(max_length=50, unique=True, editable=False)
    email      = models.EmailField(unique=True, null=False, blank=False)
    mobile_no  = models.CharField(max_length=10, unique=True, null=True, blank=True)

    # Profile info
    first_name = models.CharField(max_length=30, blank=True)
    last_name  = models.CharField(max_length=30, blank=True)
    address    = models.TextField(blank=True, null=True)
    pin_code   = models.CharField(max_length=6, blank=True, null=True)

    # Permissions
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)

    # Tracking
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Manager
    objects = CustomUserManager()

    # Authentication
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []

    # ----------------------------------------------------------------
    # Overrides
    # ----------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Ensure a unique username is always generated before saving."""
        if not self.username:
            proposed_username = generate_random_username(self.first_name)
            while CustomUser.objects.filter(username=proposed_username).exists():
                proposed_username = generate_random_username(self.first_name)
            self.username = proposed_username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or self.username
