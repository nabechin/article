from django.db import models
from django.conf import settings


class Article(models.Model):
    content = models.TextField(max_length=1000,blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


class Comment(models.Model):
    content = models.TextField(max_length=500,blank=True)
    article = models.ForeignKey(
         'Article',
         on_delete=models.CASCADE,
         null = True,
         related_name='comment'
     )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null = True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.content


class FavoriteArticle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null = True,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
         'Article',
         on_delete=models.CASCADE,
         null = True,
         related_name='favorite_article'
     )


class FavoriteComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null = True,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
         'Comment',
         on_delete=models.CASCADE,
         null = True,
         related_name='favorite_comment'
    )




