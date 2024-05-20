import uuid

from django.db import models


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, unique=True, blank=True, default=""
    )
    participants = models.ManyToManyField("user.User")

    def __str__(self):
        return str(self.id)
