from django.urls import path, include
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from . import views


app_name = 'api'


router = DefaultRouter()
router.register('profileEdit', views.UserProfileEditView)
router.register('relation', views.RelationView)
router.register('commentForArticle', views.CommentForArticle)
router.register('favoriteArticle', views.FavoriteArticleView)
router.register('favoriteComment', views.FavoriteCommentView)
router.register('message', views.SendMessageView)

urlpatterns = [
    path('', include(router.urls)),
]
