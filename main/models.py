from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, mobile_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must provide a first name")
        if not mobile_number:
            raise ValueError("Users must provide a mobile number")

        email = self.normalize_email(email)

        # Generate username: FirstName + last 4 digits of mobile
        base_username = first_name.capitalize()
        last_digits = mobile_number[-4:]
        username = f"{base_username}{last_digits}"

        # Ensure uniqueness
        counter = 1
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}{last_digits}{counter}"
            counter += 1

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(first_name, last_name, email, mobile_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True, blank=True)  # Auto-generated
    mobile_number = models.CharField(max_length=15, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "mobile_number"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
