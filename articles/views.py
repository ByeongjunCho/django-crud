from django.shortcuts import render, redirect, get_object_or_404
from IPython import embed
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
# from accounts.models import User
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.contrib.auth import get_user_model 
from IPython import embed

from .forms import ArticleForm, CommentForm
from .models import Article, Comment, HashTag
# Create your views here.
def index(request):
    articles = Article.objects.order_by('-id')
    context = {
        'articles': articles
    }
    # embed()
    return render(request, 'articles/index.html', context)

# def new(request):
#     if request.method == 'GET':
#         return render(request, 'articles/new.html')
    
@login_required
def create(request):
    # if not request.user.is_authenticated:
    #     messages.error(request, '로그인해')
    #     return redirect('articles:index')

    if request.method == 'POST':
    # POST 요청 -> 검증 및 저장 로직
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
        # 검증에 성공하면 저장
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            article = article_form.save(commit=False)
            article.user = request.user  # User class의 객체
            article.save()
            
            # 해시태그 저장 및 연결 작업
            for word in article.content.split():
                if word.startswith('#'):
                    hashtag, created = HashTag.objects.get_or_create(content=word)
                    article.hashtags.add(hashtag)
                    # if HashTag.objects.filter(content=word).exists():
                    #     hashtag = HashTag.objects.get(content=word)
                    # try:
                    #     hashtag = HashTag.objects.get(content=word)
                    # except:
            # article = article_form.save(commit=False)
            # article.image = request.FILES.get('image')
            # embed()
            # article.save()
            
            return redirect('articles:detail', article.pk)
        # else:
            # return form -> 중복되서 제거
    else:
        # GET 요청 -> Form
        article_form = ArticleForm()
    # GET -> 비어있는 Form context
    # POST -> 검증 실패시 에러메세지와 입력값 다시 context
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)


def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    a = ['22', '33', '44']
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'a': a
    }
    return render(request, 'articles/detail.html', context)



@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if article.user == request.user:
    # if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    else:
        raise PermissionDenied
    # else:
    #     return redirect('articles:detail', article_pk)

# def edit(request, article_pk):
#     if request.method == 'GET':
#         article = Article.objects.get(pk=article_pk)
#         context = {
#             'article': article
#         }
#         return render(request, 'articles/edit.html', context)
#     else:
#         article = Article.objects.get(pk=article_pk)
#         article.title = request.POST.get('title')
#         article.content = request.POST.get('content')
#         article.save()
#         return redirect('articles:detail', article.pk)    

def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        # if request.user != article.user:
            # return redirect('articles:detail', article_pk)
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, instance=article)   # 수정할 대상이 article이기 때문에 instance로 입력 설정
            if article_form.is_valid():
                # article.title = article_form.cleaned_data.get('title')
                # article.content = article_form.cleaned_data.get('content')
                # article.save()
                article = article_form.save()
                # 해시태그 수정
                article.hashtags.clear()
                for word in article.content.split():
                    if word.startswith('#'):
                        hashtag, created = HashTag.objects.get_or_create(content=word)
                        article.hashtags.add(hashtag)
                return redirect('articles:detail', article.pk)
        else:
            # article_form = ArticleForm(
            #     initial={
            #         'title': article.title,
            #         'content': article.content
            #         }
            #     )
            article_form = ArticleForm(instance=article)
        context = {
            'article': article,
            'article_form':article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        return HttpResponseForbidden()

@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        # 1. modelform에 사용자 입력값 넣고
        comment_form = CommentForm(request.POST)  # ModelForm instance
        # 2. 검증
        if comment_form.is_valid():
            # 3. 맞으면 저장
            # 3-1. 사용자 입력값으로 comment instance 생성 (저장은 X)
            comment = comment_form.save(commit=False)  # comment object로 리턴된다.
            # 3-2. Foreign key를 입력하고 저장
            comment.article = article
            comment.user = request.user
            comment.save()  # DB에 쿼리
            # 4. return redirect
        else:
            messages.success(request, '댓글이 형식이 맞지 않습니다.')
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponse('Unauthorized', status=401)
    # article = Article.objects.get(pk=article_pk)
    # comment = Comment()
    # comment.content = request.POST.get('comment_content')
    # comment.article = article
    # comment.article_id = article_pk
    # comment.save()
    # return redirect('articles:detail', article.pk)



@require_POST
@login_required
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        # messages.add_message(request, messages.INFO, '댓글이 삭제 되었습니다.')
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponseForbidden()

@login_required
def like(request, article_pk):
    # 좋아요를 눌렀다면
    article = Article.objects.get(pk=article_pk)
    if request.user in article.like_users.all():
        # 좋아요 취소 로직
        article.like_users.remove(request.user)
    # 아니면
    else:
        # 좋아요 로직
        article.like_users.add(request.user)
    return redirect('articles:detail', article_pk)

def hashtag(request, tag_pk):
    hashtag = get_object_or_404(HashTag, pk=tag_pk)
    context = {
        'hashtag': hashtag
    }
    return render(request, 'articles/hashtag.html', context)