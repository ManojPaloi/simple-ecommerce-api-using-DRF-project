# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Full User Serializer

    - Serializes all fields of `CustomUser`.
    - Safe for API responses because sensitive fields (like password) 
      are write-only and admin flags are read-only.
    """

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},   # never return password in API
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
            "groups": {"read_only": True},
            "user_permissions": {"read_only": True},
        }


class RegisterSerializer(serializers.ModelSerializer):
    """
    User Registration Serializer

    - Validates and creates new users.
    - Requires a minimum 6-character password.
    - Exposes only safe fields for registration (no admin flags).
    """
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile_no",
            "address",
            "pin_code",
            "password",
        ]

    def create(self, validated_data):
        # Extract password separately since `create_user` handles hashing
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    User Login Serializer

    - Accepts email and password.
    - Uses Django's `authenticate` to check credentials.
    - Returns the authenticated user if valid, else raises error.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        # Authenticate user with provided credentials
        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data["user"] = user
        return data


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Profile Update Serializer

    - Allows editing personal details of a user.
    - Username is read-only (cannot be changed after registration).
    """
    username = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "mobile_no",
            "address",
            "pin_code",
        ]

    def update(self, instance, validated_data):
        # Apply updates to allowed fields only
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
