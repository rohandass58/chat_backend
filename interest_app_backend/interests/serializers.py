from rest_framework import serializers
from .models import Interest, Message


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["receiver", "status"]  # Add any other fields you need
        read_only_fields = ["sender"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["sender"] = request.user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "content",
            "created_at",
        ]
