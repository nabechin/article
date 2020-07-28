from channels.generic.websocket import AsyncWebsocketConsumer
# from django.db import connection
from django.db.utils import OperationalError
from channels.db import database_sync_to_async
from django.core import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
import json
from .models import TalkRoom, Message
from account.models import UserProfile
from urllib.parse import urlparse
from pytz import timezone
from dateutil import parser
import datetime
import time


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        try:
            await self.accept()
            self.room_group_name = self.scope['url_route']['kwargs']['room_id']
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            raise

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            body = text_data_json['body']
            sender = text_data_json['sender']
            create_at = text_data_json['create_at']
            await self.createMessage(text_data_json)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': body,
                    'name': sender,
                    'create_at': create_at,
                }
            )
        except Exception as e:
            raise

    async def chat_message(self, event):
        try:
            body = event['message']
            sender = get_user_model().objects.get(pk=int(event['name']))
            user_profile = UserProfile.objects.get(user__id=int(event['name']))
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'body': body,
                'name': sender.name,
                'sender': sender.id,
                'create_at':   str(parser.parse(event['create_at']).astimezone(timezone('Asia/Tokyo'))),
                'profile_image': str(user_profile.profile_image.url),
                'talk_room_id': self.room_group_name,
            }))
        except Exception as e:
            raise

    @database_sync_to_async
    def createMessage(self, event):
        try:
            talk_room_id = TalkRoom.objects.get(
                id=self.room_group_name
            )
            sender = self.scope["user"]
            Message.objects.create(
                talk_room=talk_room_id,
                sender=sender,
                body=event['body'],
                create_at=event['create_at']
            )
        except Exception as e:
            raise
