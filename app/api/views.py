from django.shortcuts import render
from django.db.models import Q
from .serializers import UserProfileSerializer, RelationSerializer, CommentSerializer, FavoriteArticleSerializer, FavoriteCommentSerializer, MessageSerializer
from account.models import UserProfile, Relation
from article.models import Article, Comment, FavoriteArticle, FavoriteComment
from message.models import TalkRoom, Message, UserOwnTalkRoom

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.user.id
        if user_id:
            queryset = queryset.select_related('user').filter(user__id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSearchView(UserProfileView):
    def get_queryset(self):
        queryset = self.queryset
        keyword = self.request.query_params.get('keyword', None)
        if keyword:
            queryset = queryset.select_related('user').filter(
                Q(user__name__istartswith=keyword) | Q(user__username__istartswith=keyword))
        else:
            queryset = None
        return queryset


class RelationView(viewsets.ModelViewSet):
    serializer_class = RelationSerializer
    queryset = Relation.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteArticleView(viewsets.ModelViewSet):
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        talk_room_id = self.request.query_params.get('talkroom')
        if talk_room_id:
            queryset = queryset.filter(talk_room=talk_room_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
