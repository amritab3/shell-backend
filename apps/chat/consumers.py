import json

from django.db.models import Q
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ChatRoom


def combine_ids(id1, id2):
    return "".join(sorted([id1, id2]))


class ChatConsumer(AsyncWebsocketConsumer):
    http_user = True

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        from_id = self.scope.get("url_route")["kwargs"]["from_id"]
        to_id = self.scope.get("url_route")["kwargs"]["to_id"]
        combined_id = combine_ids(from_id, to_id)
        chat_room = await self.create_chat_room(combined_id, [from_id, to_id])

        self.room_name = chat_room.id
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        await self.disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        sender_id = data["sender"]
        sender = await self.get_user(sender_id)

        print(message, sender_id, sender)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )

    @database_sync_to_async
    def get_user(self, user_id):
        return get_user_model().objects.get(id=user_id)

    @database_sync_to_async
    def create_chat_room(self, room_name, participant_ids):
        chat_room, created = ChatRoom.objects.get_or_create(
            Q(name=room_name) | Q(participants=participant_ids)
        )
        if created:
            chat_room.participants.set(participant_ids)
        return chat_room
