from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.chat.models import ChatRoom, ChatMessage
from apps.chat.serializers import ChatRoomSerializer, ChatMessageSerializer
from apps.user.models import User


# Create your views here.
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated,)

    @action(
        detail=False,
        methods=["GET"],
        url_path="user-rooms",
        url_name="user-rooms",
    )
    def get_user_chat_rooms(self, request):
        request_user = request.user
        user_rooms = ChatRoom.objects.filter(
            participants__id__exact=request_user.id
        )
        serializer = ChatRoomSerializer(user_rooms, many=True)

        response_data = []
        for chat_room in serializer.data:
            for participant in chat_room["participants"]:
                if participant != request_user.id:
                    receiver = User.objects.get(id=participant)
                    response_data.append(
                        {
                            "id": chat_room["id"],
                            "name": chat_room["name"],
                            "receiver": {
                                "id": participant,
                                "name": receiver.first_name
                                + " "
                                + receiver.last_name,
                            },
                        }
                    )

        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=["GET"], url_path="messages", url_name="messages"
    )
    def get_messages(self, request, pk=None):
        room = self.get_object()

        room_messages = ChatMessage.objects.filter(room=room)
        serializer = ChatMessageSerializer(room_messages, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
