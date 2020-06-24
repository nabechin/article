from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile,Relation
from article.models import Article, FavoriteArticle
from rest_framework import viewsets
from .serializers import UserProfileSerializer,RelationSerializer
from rest_framework import permissions 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseRedirect
from typing import NamedTuple
from django.db.models import Count, Exists
from article.views import CustomArticle


# Create your views here.
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


class Logout(LoginRequiredMixin,LogoutView):
    template_name = 'logout.html'


class Profile(LoginRequiredMixin,TemplateView):
    UNFOLLOW = 0
    FOLLOW = 1
    template_name = 'profile.html'
    raise_exception = True
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        login_user = self.request.user
        user_id = kwargs['user_id']
        article_list = Article.objects.all().prefetch_related('comment').filter(user__id=user_id)
        custom_article_list = []
        for article in article_list:
            custom_article = CustomArticle(article)
            custom_article.is_login_user_like(login_user.id)
            custom_article_list.append(custom_article)
        user_profile = UserProfile.objects.select_related('user').get(user__id=user_id)
        context = super(Profile, self).get_context_data(**kwargs)
        user = get_user_model().objects.get(pk=user_id)
        relation = Relation.objects.filter(follower=login_user.id,target=user_id)
        number_of_follow = Relation.objects.filter(follower=user_id,is_deleted=False).count()
        number_of_follower = Relation.objects.filter(target=user_id,is_deleted=False).count()
        if not relation:
            context['is_follow'] = self.UNFOLLOW
        else:
            if relation[0].is_deleted:
                context['is_follow'] = self.UNFOLLOW
            else: 
                context['is_follow'] = self.FOLLOW
            context['relation'] = relation[0]
        context['number_of_follow'] = number_of_follow
        context['number_of_follower'] = number_of_follower
        context['custom_article_list'] = custom_article_list
        context['user'] = user
        context['login_user'] = login_user
        context['user_profile'] = user_profile
        return render(self.request, self.template_name,context)


class RelationView(viewsets.ModelViewSet):
    serializer_class = RelationSerializer
    permissions_classes = (permissions.IsAuthenticated)
    queryset = Relation.objects.all()

    def perform_create(self,serializer):
        target_id = serializer.validated_data.get('target',None)
        follower_id = self.request.user
        relation = Relation.objects.filter(follower=follower_id,target=target_id)
        if relation.exists():
            relation = Relation.objects.get(follower=follower_id,target=target_id)
            relation.is_deleted = False
            relation.save()
        else:
            serializer.save(follower=follower_id)


class RelationDto:
    def __init__(self,relation_profile,is_follow,relation):
        self.relation_profile = relation_profile
        self.is_follow = is_follow
        self.relation = relation


class FollowerView(LoginRequiredMixin,TemplateView):
    #htmlのフォロー、フォロワーボタンの表示、非表示で使用
    UNFOLLOW = 0
    FOLLOW = 1
    template_name = 'follower.html'
    permission_classes = (permissions.IsAuthenticated)

    def get(self,request,*args,**kwargs):
        user_id = kwargs['user_id']
        login_user = self.request.user
        relation_list = Relation.objects.filter(target=user_id,is_deleted=False)
        follower_dto_list = []

        #　パラメータのユーザのフォロワーを取得
        #　ログインユーザがリクエストパラメータユーザのフォロワーをフォローしていればis_follow -> 1
        for follower in relation_list:
            follower_id = follower.follower.id
            relation_profile = UserProfile.objects.get(user__id=follower_id)
            relation = Relation.objects.filter(follower=login_user.id,target=follower_id)
            if not relation:
                is_follow = self.UNFOLLOW
                follower_dto = RelationDto(relation_profile,is_follow,None)
            else:
                if relation[0].is_deleted:
                    is_follow = self.UNFOLLOW
                    follower_dto = RelationDto(relation_profile,is_follow,relation[0])
                else: 
                    is_follow = self.FOLLOW
                    follower_dto = RelationDto(relation_profile,is_follow,relation[0])
            follower_dto_list.append(follower_dto)
        context = super(FollowerView, self).get_context_data(**kwargs)
        context['follower_dto_list'] = follower_dto_list
        context['login_user'] = login_user
        context['user_id'] = user_id
        return render(self.request, self.template_name, context)


class FollowingView(LoginRequiredMixin,TemplateView):
    #htmlのフォロー、フォロワーボタンの表示、非表示で使用
    UNFOLLOW = 0
    FOLLOW = 1
    template_name = 'following.html'
    permission_classes = (permissions.IsAuthenticated)

    def get(self,request,*args,**kwargs):
        user_id = kwargs['user_id']
        login_user = self.request.user
        relation_list = Relation.objects.filter(follower=user_id,is_deleted=False)
        following_dto_list = []

        #　パラメータのユーザのフォローユーザを取得
        #　ログインユーザがリクエストパラメータユーザのフォローユーザをフォローしていればis_follow -> 1
        for following in relation_list:
            follower_id = following.target.id
            relation_profile = UserProfile.objects.get(user__id=follower_id)
            relation = Relation.objects.filter(follower=login_user.id,target=follower_id)
            if not relation:
                is_follow = self.UNFOLLOW
                following_dto = RelationDto(relation_profile,is_follow,None)
            else:
                if relation[0].is_deleted:
                    is_follow = self.UNFOLLOW
                    following_dto = RelationDto(relation_profile,is_follow,relation[0])
                else: 
                    is_follow = self.FOLLOW
                    following_dto = RelationDto(relation_profile,is_follow,relation[0])
            following_dto_list.append(following_dto)
        context = super(FollowingView, self).get_context_data(**kwargs)
        context['following_dto_list'] = following_dto_list
        context['login_user'] = login_user
        context['user_id'] = user_id
        return render(self.request, self.template_name, context)



class LikeArticleView(Profile):
    template_name = "like.html"

    def get(self,request,*args,**kwargs):
        login_user = self.request.user
        user_id = kwargs['user_id']
        sub_query = FavoriteArticle.objects.filter(user=login_user.id).values('article')
        favorite_article_ids = FavoriteArticle.objects.values('article__id').filter(article__in = sub_query)
        article_list = Article.objects.filter(pk__in=favorite_article_ids)
        custom_article_list = []
        for article in article_list:
            custom_article = CustomArticle(article)
            custom_article.is_login_user_like(login_user.id)
            custom_article_list.append(custom_article)
        # article_idに対応するArticleとそのfavoriteが１対１になるDTOを用意しリスト化
        user_profile = UserProfile.objects.select_related('user').get(user__id=user_id)
        context = super(LikeArticleView, self).get_context_data(**kwargs)
        user = get_user_model().objects.get(pk=user_id)
        relation = Relation.objects.filter(follower=login_user.id,target=user_id)
        number_of_follow = Relation.objects.filter(follower=user_id,is_deleted=False).count()
        number_of_follower = Relation.objects.filter(target=user_id,is_deleted=False).count()
        if not relation:
            context['is_follow'] = self.UNFOLLOW
        else:
            if relation[0].is_deleted:
                context['is_follow'] = self.UNFOLLOW
            else: 
                context['is_follow'] = self.FOLLOW
            context['relation'] = relation[0]
        context['number_of_follow'] = number_of_follow
        context['number_of_follower'] = number_of_follower
        context['custom_article_list'] = custom_article_list
        context['user'] = user
        context['login_user'] = login_user
        context['user_profile'] = user_profile
        return render(self.request, self.template_name,context)

        





