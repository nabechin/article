from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from .models import Article, Comment, FavoriteArticle, FavoriteComment
from account.serializers import UserProfileSerializer, RelationSerializer
from account.models import UserProfile, Relation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'article')


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


class FavoriteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteComment
        fields = ('id', 'user', 'comment')
