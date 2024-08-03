from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat.consumers import TextRoomConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", TextRoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
