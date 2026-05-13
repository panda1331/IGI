from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from news.models import Article

def articles(request):
    all_articles = Article.objects.all()
    return render(request, 'news/articles.html', context={'articles': all_articles})

def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponseNotFound("Article does not exist")

    return render(request, 'news/article_info.html', context={'article': article})

