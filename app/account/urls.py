from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from . import views


app_name = 'account'
router = DefaultRouter()
router.register('profileEdit', views.UserProfileEditView)
router.register('relation', views.RelationView)


urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.UserRegisterView.as_view(), name='signup'),
    path('profile/<int:user_id>', views.UserProfileView.as_view(), name='profile'),
    path('follower/<int:user_id>', views.FollowerView.as_view(), name='follower'),
    path('following/<int:user_id>',
         views.FollowingView.as_view(), name='following'),
    path('like/<int:user_id>', views.LikeArticleView.as_view(), name='like'),
    path('media/<int:user_id>', views.ArticleMedia.as_view(), name='media'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
