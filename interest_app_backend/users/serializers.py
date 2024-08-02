from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import *
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "phone_number", "password"]

    def create(self, validated_data):
        # Extract password from validated_data
        password = validated_data.pop("password")

        # Create user instance with the remaining data
        user = CustomUser.objects.create(phone_number=validated_data["phone_number"])

        # Set the password using the set_password method to hash it
        user.set_password(password)

        # Save the user instance
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "phone_number",
        ]  # Add other fields as needed
