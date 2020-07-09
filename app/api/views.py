from django.shortcuts import render
from .serializers import UserProfileSerializer, RelationSerializer, CommentSerializer, FavoriteArticleSerializer, FavoriteCommentSerializer, MessageSerializer
from account.models import UserProfile, Relation
from article.models import Article, Comment, FavoriteArticle, FavoriteComment
from message.models import TalkRoom, Message, UserOwnTalkRoom

from rest_framework import viewsets
from rest_framework import permissions


class UserProfileEditView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.user.id
        if user_id:
            queryset = queryset.select_related('user').filter(user__id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RelationView(viewsets.ModelViewSet):
    serializer_class = RelationSerializer
    permissions_classes = (permissions.IsAuthenticated)
    queryset = Relation.objects.all()

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class CommentForArticle(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteArticleView(viewsets.ModelViewSet):
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    permission_class = (permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article=article_id)
        return queryset


class FavoriteCommentView(viewsets.ModelViewSet):
    serializer_class = FavoriteCommentSerializer
    queryset = FavoriteComment.objects.all()
    permission_class = (permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SendMessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        talk_room_id = self.request.query_params.get('talkroom')
        if talk_room_id:
            queryset = queryset.filter(talk_room=talk_room_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)