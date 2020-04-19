from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from .models import Article, Notice


class ArticleView(TemplateView):
    template_name = "article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_id = context["article_id"]
        context["article"] = get_object_or_404(Article, pk=article_id)
        return context

class NoticeView(TemplateView):
    template_name = "notice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notice_id = context["notice_id"]
        context["article"] = get_object_or_404(Notice, pk=notice_id)
        return context

class GuideView(TemplateView):
    template_name = "help_guide.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter(pk__gt=1)
        return context

class SiteNoticesView(TemplateView):
    template_name = "help_notice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notices"] = Notice.objects.all()
        return context
