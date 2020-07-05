from django.db import models
from django.conf import settings
# Create your models here.


class TalkRoom(models.Model):
    last_message = models.CharField(
        max_length=255,
        blank=True,
    )


class UserOwnTalkRoom(models.Model):
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null = True,
        on_delete=models.CASCADE,
        related_name='participant',
    )
    talk_room = models.ForeignKey(
        'TalkRoom',
        null = True,
        on_delete=models.CASCADE,
    )


class Message(models.Model):
    talk_room = models.ForeignKey(
        'TalkRoom',
        null = True,
        on_delete=models.CASCADE,
    )
    body = models.CharField(
        max_length=255,
        blank=True,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null = True,
        on_delete=models.CASCADE,
        related_name='sender',
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )

