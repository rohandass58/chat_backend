from django.urls import path
from .views import SendInterestAPI, AcceptRejectInterestAPI, SendMessageAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(
        "send-interest/",
        SendInterestAPI.as_view(),
        name="send-interest",
    ),
    path(
        "accept-reject-interest/",
        AcceptRejectInterestAPI.as_view(),
        name="accept-reject-interest",
    ),
    path(
        "send-message/",
        SendMessageAPI.as_view(),
        name="send-message",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
