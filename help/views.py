from django.shortcuts import render, get_object_or_404
from .models import Article, Notice


def article(request, article_id):
    site_article = get_object_or_404(Article, pk=article_id)
    return render(request, 'article.html', {'article': site_article})


def notice(request, notice_id):
    site_notice = get_object_or_404(Notice, pk=notice_id)
    return render(request, 'notice.html', {'notice': site_notice})


def site_help(request):
    notices = Notice.objects.all()
    context = {
        'notices': notices,
    }
    return render(request, 'help_table.html', context)

# Create your views here.
