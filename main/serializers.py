from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "mobile_number", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data.get("last_name", ""),
            email=validated_data["email"],
            mobile_number=validated_data["mobile_number"],
            password=validated_data["password"]
        )
        return user

    def to_representation(self, instance):
        """Customize response to include generated username"""
        rep = super().to_representation(instance)
        rep["username"] = instance.username
        return rep


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "email", "username", "mobile_number", "date_joined")
