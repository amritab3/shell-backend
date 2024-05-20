from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from apps.chat.views import ChatRoomViewSet

router = DefaultRouter()

router.register(r"chat-rooms", ChatRoomViewSet, basename="chat-rooms")

urlpatterns = [
    path("", include(router.urls)),
]
