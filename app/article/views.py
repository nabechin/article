from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, TemplateView

from .forms import ArticleForm
from .models import Article
from .article_info import ArticleInfo

from account.models import Relation, UserProfile
from app.dto import RelationInfo


class ArticleList(LoginRequiredMixin, TemplateView):
    model = Article
    template_name = 'article_list.html'

    def get(self, request, *args, **kwargs):
        login_user_id = self.request.user.id
        login_user_following = Relation.objects.filter(follower=login_user_id)
        login_user_following_ids = [
            relation.target.id for relation in login_user_following]
        article_list = Article.objects.filter(
            Q(user__id__in=login_user_following_ids) | Q(user__id=login_user_id)).order_by('-id')
        article_info_list = []
        for article in article_list:
            article_info = ArticleInfo(article)
            article_info.is_login_user_like(login_user_id)
            article_info_list.append(article_info)
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['article_info_list'] = article_info_list
        context['user_profile'] = UserProfile.objects.get(
            user__id=login_user_id)
        return render(self.request, self.template_name, context)


class CommentOfArticle(TemplateView):
    model = Article
    template_name = 'comment_of_article.html'

    def get(self, request, *args, **kwargs):
        login_user_id = self.request.user.id
        article = Article.objects.get(id=kwargs['article_id'])
        article_info = ArticleInfo(article)
        article_info.is_login_user_like(login_user_id)
        article_info.is_login_user_like_comment(login_user_id)
        context = super(CommentOfArticle, self).get_context_data(**kwargs)
        context['article_info'] = article_info
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_user_model().objects.get(pk=self.request.user.id)
        return context


class ArticlePostView(CreateView):
    model = Article
    form_class = ArticleForm
    success_url = '/article/'
    template_name = 'article_list.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        content = self.object.content
        article = Article(content=content)
        if self.request.FILES:
            article.article_media = self.request.FILES['article_media']
        article.user = self.request.user
        article.save()
        return redirect(self.get_success_url())
