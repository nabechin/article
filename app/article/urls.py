from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'article'

urlpatterns = [
    path('', views.ArticleList.as_view(), name='article'),
    path('comment/<int:article_id>',
         views.CommentOfArticle.as_view(), name='comment'),
    path('post/', views.ArticlePostView.as_view(), name='post'),
]
