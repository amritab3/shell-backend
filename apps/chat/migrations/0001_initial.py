# Generated by Django 4.2.6 on 2024-05-19 17:09

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, default="", max_length=255, unique=True
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]
