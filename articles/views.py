from django.shortcuts import render

# Create your views here.
from .models import Article
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)