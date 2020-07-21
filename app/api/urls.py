from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'api'


router = DefaultRouter()
router.register('relation', views.RelationView)
router.register('user_profile', views.UserProfileView)
router.register('comment', views.CommentView)
router.register('favorite_article', views.FavoriteArticleView)
router.register('favorite_comment', views.FavoriteCommentView)
router.register('message', views.MessageView)

urlpatterns = [
    path('', include(router.urls))
]
