from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField


from account.models import UserProfile, Relation
from article.models import Article, Comment, FavoriteArticle, FavoriteComment
from message.models import Message, TalkRoom


'''ユーザ情報に関するserializer'''


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'name',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('introduction', 'profile_image', 'background_image', 'user',)
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.introduction = validated_data.get(
            'introduction', instance.introduction)
        instance.profile_image = validated_data.get(
            'profile_image', instance.profile_image)
        instance.background_image = validated_data.get(
            'background_image', instance.background_image)
        user_data = validated_data.get('user')
        instance.user.name = user_data.get('name')
        instance.user.save()
        instance.save()
        return instance


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('id', 'follower', 'target',)


'''記事に関するserializer'''


class FavoriteArticleSerializer(serializers.ModelSerializer):
    user_profile = SerializerMethodField()
    relation = SerializerMethodField()

    class Meta:
        model = FavoriteArticle
        fields = ('id', 'article', 'user', 'user_profile', 'relation',)

    def get_user_profile(self, obj):
        try:
            user_profile = UserProfileSerializer(UserProfile.objects.get(
                user__id=get_user_model().objects.get(id=obj.user.id).id)).data
            return user_profile
        except:
            user_profile = None
            return user_profile

    def get_relation(self, obj):
        user = self.context['request'].user
        try:
            relation = RelationSerializer(Relation.objects.all().filter(target=get_user_model(
            ).objects.get(id=obj.user.id).id, follower=user.id), many=True).data
            return relation
        except:
            relation = None
            return relation


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content', 'article')


class FavoriteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteComment
        fields = ('id', 'user', 'comment')


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
