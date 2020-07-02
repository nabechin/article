from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from account.models import Relation, UserProfile
from app.dto import RelationDto, CustomArticle
from rest_framework import permissions, viewsets

from .forms import ArticleForm
from .models import Article, Comment, FavoriteArticle, FavoriteComment
from .serializers import CommentSerializer, FavoriteArticleSerializer, FavoriteCommentSerializer
        

class ArticleList(LoginRequiredMixin,TemplateView):
    model = Article 
    template_name='article_list.html'

    def get(self,request,*args,**kwargs):
        login_user_id = self.request.user.id
        login_user_following = Relation.objects.filter(follower=login_user_id)
        login_user_following_ids = [relation.target.id for relation in login_user_following]
        article_list = Article.objects.filter(Q(user__id__in=login_user_following_ids) | Q(user__id=login_user_id)).order_by('-id')
        custom_article_list =[]
        for article in article_list:
            custom_article = CustomArticle(article)
            custom_article.is_login_user_like(login_user_id)
            custom_article_list.append(custom_article)
        context = super(ArticleList,self).get_context_data(**kwargs)
        context['custom_article_list'] = custom_article_list
        context['user_profile'] = UserProfile.objects.get(user__id=login_user_id)
        return render(self.request,self.template_name,context)


class CommentOfArticle(TemplateView):
    model = Article
    template_name='comment_of_article.html'

    def get(self,request,*args,**kwargs):
        login_user_id = self.request.user.id
        article = Article.objects.get(id=kwargs['article_id'])
        custom_article = CustomArticle(article)
        custom_article.is_login_user_like(login_user_id)
        custom_article.is_login_user_like_comment(login_user_id)
        context = super(CommentOfArticle,self).get_context_data(**kwargs)
        context['custom_article'] = custom_article
        return render(self.request,self.template_name,context)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_user_model().objects.get(pk=self.request.user.id)
        return context


class CommentForArticle(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticlePostView(CreateView):
    model = Article
    form_class = ArticleForm
    success_url = "/article/"
    template_name='article_list.html'

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return redirect(self.get_success_url())


class FavoriteArticleView(viewsets.ModelViewSet):
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    permission_class = (permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        queryset = self.queryset
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article=article_id)
        return queryset
        

class FavoriteCommentView(viewsets.ModelViewSet):
    serializer_class = FavoriteCommentSerializer
    queryset = FavoriteComment.objects.all()
    permission_class = (permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
