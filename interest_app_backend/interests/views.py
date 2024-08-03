from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Interest, Message
from .serializers import InterestSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SendInterestAPI(generics.CreateAPIView):
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class AcceptRejectInterestAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        interest_id = request.data.get("interest_id")
        new_status = request.data.get("status")  # Rename `status` to `new_status`

        try:
            interest = Interest.objects.get(id=interest_id, receiver=request.user)
            if new_status in ["accepted", "rejected"]:  # Use `new_status` here
                interest.status = new_status
                interest.save()
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Interest.DoesNotExist:
            return Response(
                {"error": "Interest not found"}, status=status.HTTP_404_NOT_FOUND
            )


class SendMessageAPI(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        receiver = serializer.validated_data.get("receiver")

        # Check if the interest is accepted
        if (
            Interest.objects.filter(
                sender=sender, receiver=receiver, status="accepted"
            ).exists()
            or Interest.objects.filter(
                sender=receiver, receiver=sender, status="accepted"
            ).exists()
        ):
            serializer.save(sender=sender)
        else:
            raise serializers.ValidationError(
                "You are not allowed to send messages to this user."
            )
