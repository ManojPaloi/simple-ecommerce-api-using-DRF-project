import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


def generate_random_username(first_name=None):
    """Generate unique username using first name + random string"""
    base = (first_name.lower() if first_name else "user")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{base}_{random_str}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_no=None, password=None, first_name=None, **extra_fields):
        """
        Create and return a regular user.
        """
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)

        # Auto-generate username if not given
        if not extra_fields.get("username"):
            proposed_username = generate_random_username(first_name)
            while CustomUser.objects.filter(username=proposed_username).exists():
                proposed_username = generate_random_username(first_name)
            extra_fields["username"] = proposed_username

        user = self.model(
            email=email,
            mobile_no=mobile_no,
            first_name=first_name or "",
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    mobile_no = models.CharField(max_length=10, unique=True, null=True, blank=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)

    # Permissions
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    # For authentication
    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = []       

    def save(self, *args, **kwargs):
        """Ensure username is unique when saving"""
        if not self.username:
            proposed_username = generate_random_username(self.first_name)
            while CustomUser.objects.filter(username=proposed_username).exists():
                proposed_username = generate_random_username(self.first_name)
            self.username = proposed_username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or self.username
