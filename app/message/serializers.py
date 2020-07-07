from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from account.serializers import UserProfileSerializer
from account.models import UserProfile
from .models import Message, TalkRoom


class MessageSerializer(serializers.ModelSerializer):
    user_profile = SerializerMethodField()

    class Meta:
        model = Message
        fields = ('talk_room', 'body', 'sender', 'create_at', 'user_profile',)

    def create(self, validated_data):
        talk_room = TalkRoom.objects.get(id=validated_data.get('talk_room').id)
        body = validated_data.get('body')
        sender = validated_data.get('sender')
        message = Message.objects.create(
            body=body, sender=sender, talk_room=talk_room)
        talk_room.last_message = body
        talk_room.save()
        return message

    def get_user_profile(self, obj):
        try:
            user_profile = UserProfileSerializer(
                UserProfile.objects.get(user__id=obj.sender.id)).data
            return user_profile
        except:
            user_profile = None
            return user_profile
