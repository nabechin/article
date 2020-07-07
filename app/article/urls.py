from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'article'
router = DefaultRouter()
router.register('commentForArticle', views.CommentForArticle)
router.register('favoriteArticle', views.FavoriteArticleView)
router.register('favoriteComment', views.FavoriteCommentView)


urlpatterns = [
    path('', views.ArticleList.as_view(), name='article'),
    path('comment/<int:article_id>',
         views.CommentOfArticle.as_view(), name='comment'),
    path('post/', views.ArticlePostView.as_view(), name='post'),
    path('', include(router.urls)),
]
