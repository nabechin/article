from rest_framework import serializers
from .models import Comment, FavoriteArticle, FavoriteComment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content','article')


class FavoriteArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteArticle
        fields = ('id','user','article')


class FavoriteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteComment
        fields = ('id','user','comment')