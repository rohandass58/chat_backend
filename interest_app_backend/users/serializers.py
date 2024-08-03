from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import *
from django.contrib.auth import authenticate
from interests.serializers import InterestSerializer
from interests.models import Interest


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
    sent_interest_status = serializers.SerializerMethodField()
    received_interest_status = serializers.SerializerMethodField()
    interest_id = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "phone_number",
            "sent_interest_status",
            "received_interest_status",
            "interest_id",
        ]

    def get_sent_interest_status(self, obj):
        user = self.context["request"].user
        interest = Interest.objects.filter(sender=user, receiver=obj).first()
        return interest.status if interest else None

    def get_received_interest_status(self, obj):
        user = self.context["request"].user
        interest = Interest.objects.filter(sender=obj, receiver=user).first()
        return interest.status if interest else None

    def get_interest_id(self, obj):
        user = self.context["request"].user
        interest = Interest.objects.filter(
            models.Q(sender=user, receiver=obj) | models.Q(sender=obj, receiver=user)
        ).first()
        return str(interest.id) if interest else None
