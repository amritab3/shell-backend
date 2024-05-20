from django.urls import path

from apps.chat import consumers

websocket_urlpatterns = [
    path(
        "ws/chat/from/<str:from_id>/to/<str:to_id>",
        consumers.ChatConsumer.as_asgi(),
    ),
]
