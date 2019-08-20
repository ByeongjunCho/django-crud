from django.shortcuts import render, redirect

# Create your views here.
from .models import Article
def index(request):
    articles = Article.objects.order_by('-id')

    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def new(request):
    
    return render(request, 'articles/new.html')

def create(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    article = Article(title=title, content=content)
    # article.title = title
    # article.content = content
    article.save()
    context = {
        'article': article
    }
    
    # return render(request, 'articles/create.html', context)
    return redirect(f'/articles/{article.pk}/')

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)

def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()
    return redirect('/articles/')

def edit(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/edit.html', context)

def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.title = request.GET.get('title')
    article.content = request.GET.get('content')
    article.save()

    return redirect(f'/articles/{article_pk}/')
