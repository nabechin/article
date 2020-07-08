from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count
from django.db.models import Q
from django.views.generic import TemplateView, CreateView

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .forms import UserRegisterForm, LoginForm
from .models import UserProfile, Relation
from .serializers import UserProfileSerializer, RelationSerializer

from article.models import Article, FavoriteArticle
from article.article_info import ArticleInfo
from app.dto import RelationInfo


class UserRegisterView(CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    template_name = 'signup.html'
    success_url = '/account/login/'

    def form_valid(self, form):
        del form.cleaned_data['password2']
        validate_data = form.cleaned_data
        self.object = user = get_user_model().objects.create_user(**validate_data)
        UserProfile.objects.create(user_id=user.id)
        messages.info(self.request, f'ユーザ名{user.name}さんのアカウントを作成しました')
        return redirect(self.get_success_url())


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


class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    UNFOLLOW = 0
    FOLLOW = 1
    template_name = 'profile.html'
    raise_exception = True
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        login_user = self.request.user
        user_id = kwargs['user_id']
        article_info_list = []
        article_list = Article.objects.all().prefetch_related(
            'comment').filter(user__id=user_id)
        for article in article_list:
            article_info = ArticleInfo(article)
            article_info.is_login_user_like(login_user.id)
            article_info_list.append(article_info)
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['article_info_list'] = article_info_list
        relation = Relation.objects.filter(
            follower=login_user.id, target=user_id)
        if not relation:
            context['is_follow'] = self.UNFOLLOW
        else:
            context['is_follow'] = self.FOLLOW
            context['relation'] = relation[0]
        context['number_of_follow'] = Relation.objects.filter(
            follower=user_id).count()
        context['number_of_follower'] = Relation.objects.filter(
            target=user_id).count()
        context['user'] = get_user_model().objects.get(pk=user_id)
        context['login_user'] = login_user
        context['user_profile'] = UserProfile.objects.select_related(
            'user').get(user__id=user_id)
        return render(self.request, self.template_name, context)


class RelationView(viewsets.ModelViewSet):
    serializer_class = RelationSerializer
    permissions_classes = (permissions.IsAuthenticated)
    queryset = Relation.objects.all()

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FollowerView(LoginRequiredMixin, TemplateView):
    # htmlのフォロー、フォロワーボタンの表示、非表示で使用
    UNFOLLOW = 0
    FOLLOW = 1
    template_name = 'follower.html'
    permission_classes = (permissions.IsAuthenticated)

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        login_user = self.request.user
        relation_list = Relation.objects.filter(target=user_id)
        follower_info_list = []

        #　ログインユーザにフォローしているユーザを取得
        #　ログインユーザuser_idのフォロワーをフォローしていればis_follow -> 1
        for follower in relation_list:
            follower_id = follower.follower.id
            relation_profile = UserProfile.objects.get(user__id=follower_id)
            relation = Relation.objects.filter(
                follower=login_user.id, target=follower_id)
            if not relation:
                is_follow = self.UNFOLLOW
                follower_info = RelationInfo(relation_profile, is_follow, None)
            else:
                is_follow = self.FOLLOW
                follower_info = RelationInfo(
                    relation_profile, is_follow, relation[0])
            follower_info_list.append(follower_info)
        context = super(FollowerView, self).get_context_data(**kwargs)
        context['follower_info_list'] = follower_info_list
        context['login_user'] = login_user
        context['user_id'] = user_id
        return render(self.request, self.template_name, context)


class FollowingView(LoginRequiredMixin, TemplateView):
    # htmlのフォロー、フォロワーボタンの表示、非表示で使用
    UNFOLLOW = 0
    FOLLOW = 1
    template_name = 'following.html'
    permission_classes = (permissions.IsAuthenticated)

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        login_user = self.request.user
        relation_list = Relation.objects.filter(follower=user_id)
        following_info_list = []

        #　ログインユーザがフォローしているユーザを取得
        #　ログインユーザがuser_idのフォローユーザをフォローしていればis_follow -> 1
        for following in relation_list:
            follower_id = following.target.id
            relation_profile = UserProfile.objects.get(user__id=follower_id)
            relation = Relation.objects.filter(
                follower=login_user.id, target=follower_id)
            if not relation:
                is_follow = self.UNFOLLOW
                following_info = RelationInfo(
                    relation_profile, is_follow, None)
            else:
                is_follow = self.FOLLOW
                following_info = RelationInfo(
                    relation_profile, is_follow, relation[0])
            following_info_list.append(following_info)
        context = super(FollowingView, self).get_context_data(**kwargs)
        context['following_info_list'] = following_info_list
        context['login_user'] = login_user
        context['user_id'] = user_id
        return render(self.request, self.template_name, context)


class LikeArticleView(UserProfileView):
    template_name = "like.html"

    def get(self, request, *args, **kwargs):
        login_user = self.request.user
        user_id = kwargs['user_id']
        sub_query = FavoriteArticle.objects.filter(
            user=user_id).values('article')
        favorite_article_ids = FavoriteArticle.objects.values(
            'article__id').filter(article__in=sub_query)
        article_list = Article.objects.filter(pk__in=favorite_article_ids)
        article_info_list = []
        for article in article_list:
            article_info = ArticleInfo(article)
            article_info.is_login_user_like(login_user.id)
            article_info_list.append(article_info)

        # article_idに対応するArticleとそのfavoriteが１対１になるDTOを用意しリスト化
        context = super(LikeArticleView, self).get_context_data(**kwargs)
        context['article_info_list'] = article_info_list
        relation = Relation.objects.filter(
            follower=login_user.id, target=user_id)
        if not relation:
            context['is_follow'] = self.UNFOLLOW
        else:
            context['is_follow'] = self.FOLLOW
            context['relation'] = relation[0]
        context['number_of_follow'] = Relation.objects.filter(
            follower=user_id).count()
        context['number_of_follower'] = Relation.objects.filter(
            target=user_id).count()
        context['user'] = get_user_model().objects.get(pk=user_id)
        context['login_user'] = login_user
        context['user_profile'] = UserProfile.objects.select_related(
            'user').get(user__id=user_id)
        return render(self.request, self.template_name, context)


class ArticleMedia(UserProfileView):
    template_name = 'media.html'

    def get(self, request, *args, **kwargs):
        login_user = self.request.user
        user_id = kwargs['user_id']
        article_list = Article.objects.all().prefetch_related(
            'comment').filter(user__id=user_id).exclude(article_media='')
        article_info_list = []
        for article in article_list:
            article_info = ArticleInfo(article)
            article_info.is_login_user_like(login_user.id)
            article_info_list.append(article_info)
        context = super(ArticleMedia, self).get_context_data(**kwargs)
        relation = Relation.objects.filter(
            follower=login_user.id, target=user_id)
        if not relation:
            context['is_follow'] = self.UNFOLLOW
        else:
            context['is_follow'] = self.FOLLOW
            context['relation'] = relation[0]
        context['number_of_follow'] = Relation.objects.filter(
            follower=user_id).count()
        context['number_of_follower'] = Relation.objects.filter(
            target=user_id).count()
        context['article_info_list'] = article_info_list
        context['user'] = get_user_model().objects.get(pk=user_id)
        context['login_user'] = login_user
        context['user_profile'] = UserProfile.objects.select_related(
            'user').get(user__id=user_id)
        return render(self.request, self.template_name, context)
