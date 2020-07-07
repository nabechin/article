import uuid
import os

from django.db import models
from django.conf import settings


def article_media_save_path(instance, file_name):
    extension = file_name.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    return os.path.join('article_media/', file_name)


class Article(models.Model):
    content = models.TextField(max_length=1000, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    article_media = models.ImageField(
        null=True, upload_to=article_media_save_path, default="")


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=True)
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        null=True,
        related_name='comment'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.content


class FavoriteArticle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_article'
    )


class FavoriteComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_comment'
    )
