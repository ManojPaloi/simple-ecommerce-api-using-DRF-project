# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """User serializer (all fields, safe for API response)"""

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},   # never expose password
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
            "groups": {"read_only": True},
            "user_permissions": {"read_only": True},
        }


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = [ "first_name", "last_name","email", "mobile_no", "address", "pin_code", "password" ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login with email + password"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

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
    """Serializer for updating user profile (username read-only)"""
    username = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "mobile_no", "address", "pin_code"]

    def update(self, instance, validated_data):
        # username is read_only, so it won't be updated
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



