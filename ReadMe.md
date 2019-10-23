# Django - CRUD

> Django ORM을 활용하여 게시판 기능 구현하기

## 1. 환경설정

* 가상환경(venv)

  * python 3.7.4에서 가상환경 생성

    ```bash
    $ python -V
    python 3.7.4
    $ python -m venv venv
    ```

  * 가상환경 실행

    ```bash
    $ source venv/Scripts/activate
    (venv) $ 
    ```

  * 가상환경 종료

    ```bash
    (venv) $ deactivate
    ```

    

* pip - `requirements.txt` 확인

  * 현재 패키지 리스트 작성

    ```bash
    $ pip freeze > requirements.txt
    ```

  * 만약, 다른 환경에서 동일하게 설치한다면

    ```bash
    $ pip install -r requiremets.txt
    ```

* django app - `articles` 

## 2. Model 설정

### 1. `Article` 모델 정의

```python
# articles/models.py

class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

* 클래스 정의할 때는 `models.Model` 을 상속받아 만든다.

* 정의하는 변수는 실제 데이터베이스에서 각각의 필드(column)을 가지게 된다.

* 주요 필드

  * `CharField(max_length)` 
    * 필수 인자로 `max_length`를 지정하여야 한다.
    * 일반적으로 데이터베이스에서 `VARCHAR` 로 지정된다.
    * `<input type="text">`
  * `TextField()`
    * 일반적으로 데이터베이스에서 `TEXT` 으로 지정된다.
    * `CharField` 보다 더 많은 글자를 저장할 때 사용된다.
    * `<textarea>`
  * `DateTimeField()`
    * 파이썬의 datetime 객체로 활용된다.
    * 옵션
      * `auto_now_add=True` : 생성시에 자동으로 저장(게시글 작성일)
      * `auto_now=True` : 변경시에 자동으로 저장(게시글 수정일)
  * `BooleanField()`, `FileField()` , `IntegerField()` 등 다양한 필드를 지정할 수 있다.

* `id` 는 자동으로 `INTEGER` 타입으로 필드가 생성되고, 이는 `PK (Primary Key)` 이다.

* 모든 필드는 `NOT NULL` 조건이 선언되며, 해당 옵션을 수정하려면 아래와 같이 정의할 수 있다.

  ```python
  username = models.CharField(max_length=10, null=True)
  ```

### 2. 마이그레이션(migration) 파일 생성

>  마이그레이션(migration)은 모델에 정의한 내용(데이터베이스의 스키마)의 변경사항을 관리한다.

따라서, 모델의 필드 수정 혹은 삭제 등이 변경될 때마다 마이그레이션 파일을 생성하고 이를 반영하는 형식으로 작업한다.

```bash
$ python manage.py makemigrations
Migrations for 'articles':
  articles\migrations\0001_initial.py
    - Create model Article
```

* 만약, 현재 데이터베이스에 반영되어 있는 마이그레이션을 확인하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py showmigrations
  articles
   [ ] 0001_initial
  ```

### 3. DB 반영(migrate)

> 만들어진 마이그레이션 파일을 실제 데이터베이스에 반영한다.

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, articles, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
```

* 만약 특정 app의 마이그레이션 혹은 특정 버전만 반영하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py migrate articles
  $ python manage.py migrate articles 0001
  ```

* 특정 마이그레이션 파일이 데이터베이스에 반영될 때 실행되는 쿼리문은 다음과 같이 확인할 수 있다.

  ```bash
  $ python manage.py sqlmigrate articles 0001
  BEGIN;
  --
  -- Create model Article
  --
  CREATE TABLE "articles_article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(10) NOT NULL, "content" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
  COMMIT;
  ```

* 데이터베이스에 테이블을 만들 때, 기본적으로 `app이름_model이름` 으로 생성된다.

## 3. Django Query Methods

> Django ORM을 활용하게 되면, 파이썬 객체 조작으로 데이터베이스 조작이 가능하다.
>
> ORM(Object-Relational-Mapping)에서는 주로 활용되는 쿼리문들이 모두 method로 구성 되어있다.

```bash
$ python manage.py shell
$ python manage.py shell_plus
```

* `shell` 에서는 내가 활용할 모델을 직접 import 해야 한다.

  ```python
  from articles.models import Article
  ```

* `shell_plus` 는 `django_extensions`를 설치 후 `INSTALLED_APPS`에 등록하고 활용해야 한다.

  ```bash
  $ pip install django-extensions
  ```

  ```python
  # crud/settings.py
  INSTALLED_APPS = [
      'django_extensions',
      ...
  ]
  ```

### 1. Create

```python
# 1. 인스턴스 생성 및 저장
article = Article()
article.title = '1번글'
article.content = '1번내용'
# article = Article(title='글', content'내용')
article.save()

# 2. create 메서드 활용
article = Article.objects.create(title='글', content='내용')
```

* 데이터베이스에 저장되면, `id` 값이 자동으로 부여된다. `.save()` 호출하기 전에는 `None` 이다.

### 2. Read

* 모든 데이터 조회

  ```python
  Article.objects.all()
  ```

  * 리턴되는 값은 `QuerySet` 오브젝트
  * 각 게시글 인스턴스들을 원소로 가지고 있다.

* 특정(단일) 데이터 조회

  ```python
  Article.objects.get(pk=1)
  ```

  * 리턴되는 값은 `Article` 인스턴스
  * `.get()` 은 그 결과가 여러개 이거나 없는 경우 오류를 발생시킴.
  * 따라서, 단일 데이터 조회시(primary key를 통해)에만 사용한다.

* 특정 데이터 조회

  ```python
  Article.objects.filter(title='제목1')
  Article.objects.filter(title__contains='제목') # 제목이 들어간 제목
  Article.objects.filter(title__startswith='제목') # 제목으로 시작하는 제목
  Article.objects.filter(title__endswith='제목') # 제목으로 끝나는 제목
  ```

  * 리턴되는 값은 `QuerySet` 오브젝트
  * `.filter()` 는 없는 경우/하나인 경우/여러개인 경우 모두 `QuerySet` 리턴

### 3. Update

```python
article = Article.objects.get(pk=1)
article.content = '내용 수정'
article.save()
```

* 수정은 특정 게시글을 데이터베이스에서 가져와서 인스턴스 자체를 수정한 후 `save()` 호출.

### 4. Delete

```python
article = Article.objects.get(pk=1)
article.delete()
```

### 5. 기타

#### 1. Limiting

```python
Article.objects.all()[0] # LIMIT 1 : 1개만
Article.objects.all()[2] # LIMIT 1 OFFSET 2 
Article.objects.all()[:3]
```

#### 2. Ordering

```python
Article.objects.order_by('-id') # id를 기준으로 내림차순 정렬
Article.objects.order_by('title') # title을 기준으로 오름차순 정렬
```

## 4. Namespace를 이용한 단순작업

* `name`키워드를 이용하여 반복작업을 쉽게 할 수 있다.

```python
# urls.py
app_name = 'articles'  # app의 이름

urlpatterns = [
    path('', views.index, name='index'),
    # ....
```

```python
return redirect('articles:detail', article.pk)
# url 작성을 한다면 python file 에도 적용 가능하다.
```

```html
...
<form action="{% url 'articles:create' %}" method="POST">
...
```

* articles - app_name | create - pathname

```html
<a href="{% url 'articles:detail' article.pk %}">
```

* name=detail에 값을 넘겨준다면 넘겨줄 값을 url 뒤에 명시한다.



## 5. GET/POST를 이용한 분기설정

```python
# views.py
def create(request):
    # 저장 로직
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article(title=title, content=content)
        article.save()
        
        return redirect('articles:detail', article.pk)
    else:
        return render(request, 'articles/new.html')
```

* 입력의 `method`에 따라 서로 다른 행동이 가능하다.

```python
from django.views.decorators.http import require_POST
@require_POST
def .....
# ....
```

* POST가 입력되는 경우만 함수가 실행되도록 할 수 있다.

```html
<form action="{% url 'articles:update' article.pk%}" method="POST">
<a href="{% url 'articles:detail' article.pk %}"></a>
```

* `<form>`태그는 `GET`과 `POST`를 변경하여 사용할 수 있다.
* `<a>`태그는 `GET`으로 고정되어 있다.

## 6.SQL 1:N

### 1. 1:N 관계 생성

```python
from django.db import models

# Create your models here.
# 1. 모델(스키마) 정의
# 데이터베이스 테이블을 정의하고,
# 각각의 컬럼(필드) 정의
class Article(models.Model):
    # id : integer 자동으로 정의(Primary Key)
    # id = models.AutoField(primary_key=True) -> Integer 값이 자동으로 하나씩 증가(AUTOINCREMENT)
    # CharField - 필수인자로 max_length 지정
    title = models.CharField(max_length=10)
    content = models.TextField()
    # DateTimeField
    #    auto_now_add : 생성시 자동으로 저장
    #    auto_now : 수정시마다 자동으로 저장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} : {self.title}'



class Comment(models.Model):
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  
    # on_delete
    # 1. CASCADE : 글이 삭제되었을 때 모든 댓글을 삭제
    # 2. PROTECT : 댓글이 존재하면 글 삭제 안됨
    # 3. SET_NULL : 글이 삭제되면 NULL로 치환(NOT NULL일 경우 옵션 사용X)
    # 4. SET_DEFAULT : 디폴트 값으로 치환.

# models.py : python 클래스 정의
#           : 모델 설계도
# makemigrations : migration 파일 생성
#           : DB 설계도 작성
# migrate : migration 파일 DB 반영

```



### 2. 데이터 활용

* 여러 방법으로 데이터 입력이 가능하다.

  ```python
  # 1. 직접 입력
  
  a = Article()
  a.title = '제목1'
  a.content = '내용1'
  
  c = Comment()
  c.content = '댓글댓글'
  c.article = a  # 객체 직접 저장
  c.reporter_id = 1 # 혹은 id를 직접 입력
  ```
  
* 각 객체가 가진 정보를 확인할 수 있다.

  ```python
  Article.objects.get(pk=1).comment.content  # '댓글댓글'
  ```

* Foreign key 확인

  ```python
  Article.objects.get(pk=1).comment_set.all() # Article(pk=1)객체를 가진 Comment객체를 모두 표시
  ```

## 7. Model Form

### 1. Model Form 정의

```python
# form.py
class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        max_length=1, 
        label='제목',
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목을 입력바랍니다.'
            }
        )
        )
    content = forms.CharField(
        # label 내용 수정
        label='내용',
        # Django form에서 HTML 속성 지정 -> widget
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'placeholder': '내용을 입력바랍니다.',
                'row': 5,
                'col': 60
            }
        )
    )
```

* 기존에 있는 모델을 form 형식으로 만들어 `HTML`에서 편하게 사용이 가능하다.

```html
<!-- article_form이 html로 넘어온 경우 -->
<form action="" method='POST'>
  {% csrf_token %}
  {{ article_form.as_p }}
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

* view.py도 간단하게 만들 수 있다.

  ```python
  # views.py
  def create(request):
      if request.method == 'POST':
      # POST 요청 -> 검증 및 저장 로직
          article_form = ArticleForm(request.POST)
          if article_form.is_valid():
          # 검증에 성공하면 저장
              article = article_form.save()
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
  ```


### 2. ModelForm save중 Foreign Key따로 저장하는 방법

```python
# views.py
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 1. modelform에 사용자 입력값 넣고
    comment_form = CommentForm(request.POST)  # ModelForm instance
    # 2. 검증
    if comment_form.is_valid():
        # 3. 맞으면 저장
        # 3-1. 사용자 입력값으로 comment instance 생성 (저장 X)
        comment = comment_form.save(commit=False)  # comment object 리턴값
        # comment = Comment()
    	# comment.content = request.POST.get('comment_content')
        
        
        # 3-2. Foreign key를 입력하고 저장
        comment.article = article
        comment.save()
        # 4. return redirect
        return redirect('articles:detail', article_pk)
```

### 3. (참고) ModelForm에서 `input`태그의 설정을 변경하는 방법

```python
# ...
class MovieForm(forms.ModelForm):
    open_date = forms.DateField(
        label = '개봉일',
        widget = forms.DateInput(attrs={
            'type': 'date'})
    )
```



## 8. static 설정

### 1. static을 위한 기본 설정

- 해당 폴더 내부에 해당 파일이 있어야 한다.
- `static`설정은 해당 Template에서만 가능하다(Django Template 불러오기는 가능하지 않음)

```python
# setting.py
# ...

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# static file들을 모두 모아서 해당 URL로 표현된다. (물리 폴더를 뜻하는 것이 아니다.)
# /static/boostarap
# /static/articles/style.css
STATIC_URL = '/static/'  

# static file 물리 위치 지정
# 기본적으로는 app에 있는 static 폴더들을 모두 관리하며, 아래에 임의의 폴더들을 추가할 수 있다.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'crud', 'assets')
]
# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
```

*  static은 기존의 데이터를 사용하는 것으로 요청에 대한 응답만 한다.

```html
<!-- ...... -->
{% load static %}
<link rel="stylesheet" href="{% static 'articles/style.css' %}">  
```

* 같은 방법으로 해당 폴더에 있는 이미지를 불러올 수 있다.

```html
<!-- ... -->
{% load static %}
<img src="{% static 'articles/gom.jpg' %}" class="rounded mx-auto d-block" alt="">
<!-- ... -->
```

## 9. 서버에 이미지 로드하기

### 1. 기본 설정

* models.ImageField() 를 사용하기 위해서는 pillow` 라이브러리가 필요하다.

  ```bash
  pip install pillow
  ```

* `models.py`에 이미지 저장을 위한 공간을 지정한다.

  ```python
  # model.py
  class Article(models.Model):
      # ...
      image = models.ImageField()
      # ...
  ```

* image저장을 위해 `views.py`에 `request`를 받을 수 있게 설정한다.

  ```python
  # views.py
  def create(request):
      # ...
      article.image = request.FILES.get('image')
      article.save()
      
      return redirect('/articles/')
  
  # django form을 사용하는 경우
  def create(request):
      if request.method == 'POST':
      # POST 요청 -> 검증 및 저장 로직
          article_form = ArticleForm(request.POST, request.FILES)  # POST와 FILES를 받아온다
          if article_form.is_valid():
          # 검증에 성공하면 저장
              article = article_form.save()
              return redirect('articles:detail', article.pk)
  ```

* `html`의 `<input>`태그를 이용해 이미지를 받을 수 있다.

* 이때, `enctype`를 꼭 설정해주어야 한다.

  ```python
  <form action="" method='POST' class="form" enctype="multipart/form-data">
  <label for="image">이미지</label>
          <input type="file" name="image" id="image">
  ```

* `setting.py`에 image를 위한 폴더 경로를 설정한다.

  ```python
  # setting.py
  # media file이 실제로 저장되는 파일의 경로
  # static 설정과 같다(폴더를 연결해야 이미지를 저장하고 보낼 수 있다.)
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  MEDIA_URL = '/media/'
  ```

* `url.py`에 url을 추가시킨다. **url설정은 꼭 필요하다.**

  ```python
  # urls.py
  from django.conf import settings
  from django.conf.urls.static import static
  # ....
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

* 이미지를 확인하고 싶다면 `html`에서 경로를 연결하여 이미지를 확인할 수 있다.

  ```html
  <img src="{{ article.image.url }}" alt="{{article.image.name}} ">
  ```

### 2. image의 크기를 조정하여 저장하기

* 이미지 설정을 변경하고 저장하기 위해서는 `imagekit` 라이브러리가 필요하다.

  ```bash
  pip install django-imagekit
  ```

* 사용을 위해서는 `setting.py`에 추가해주어야 한다.

  ```python
  # settings.py
  INSTALLED_APPS = [
      # ....
      'django_extensions',
      'bootstrap4',
      'imagekit',
  ]
  ```

* 기본 이미지의 크기를 조정하면서 저장이 가능하다.

  ```python
  from django.db import models
  from imagekit.models import ProcessedImageField, ImageSpecField
  from imagekit.processors import ResizeToFill
  
  class Article(models.Model):
      title = models.CharField(max_length=10)
      content = models.TextField()
      image = models.ImageField(blank=True)
      # ImageSpecField : Input 하나만 받고 처리해서 저장(1개의 이미지를 이용해 처리하여 저장)
      # ProcessedImageField : Input 받은 것을 처리해서 저장(여러 이미지를 입력받아 처리)
      # resize to fill : 300 * 300
      # resize to fit : 긴쪽을(너비 혹은 높이) 300에 맞추고 비율에 맞게 자름
      image_thumbnail = ImageSpecField(          # 
          processors=[ResizeToFill(300, 300)],   # 
          format='JPEG',   # format 옵션
          options={'quality': 80}  # 압축 퀄리티
      )
      
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  
      def __str__(self):
          return f'{self.id} : {self.title}'
  ```

* `ImageSpecField`는 폴더에 원본 데이터만 저장하고 요청이 들어오면 해당하는 이미지 처리를 하여 임시 폴더에 저장한다.

  ```html
  <img src="{{ article.image.url }}" alt="{{article.image.name}} ">
  <img src="{{ article.image_thumbnail.url }}" alt="{{article.image_thumbnail.name}} ">
  ```


## 10. 회원가입 생성

### 1. 기존에 존재하는 Model Form 을 이용한 생성방법

```python
# settings.py
LOGIN_URL = '/accounts/login'
AUTH_USER_MODEL = 'accounts.User'
```



```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('articles:index')
    else:
        user_form = UserCreationForm()
    context = {
        'user_form': user_form
    }
    return render(request, 'accounts/signup.html', context)
```

* 기존에 있는 `UserCreationForm`을 이용하면 간단하게 형식을 만들 수 있다.

### 2. Login in 환경 구현

```python
# accounts/views.py
from django.contrib.auth.forms import AuthenticationForm


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST) # cookie와 session을 request를 통해 넘겨준다.
        if form.is_valid():
            # 로그인
            user = form.get_user() # user를 가지고 와서
            auth_login(request, user) # login함수에 입력
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```

* `request`에는 이미 사용자 정보가 들어 있어서 context로 정보를 넘기지 않아도 `user`을 통해 사용할 수 있다.

  ```html
  <!--html의 경우 -->
  <a class="nav-link">{{ user.username }} </a>  
  ```

* Login상태를 확인해주는 메서드가 존재한다.

  ```python
  rquest.user.is_authenticated
  # request.user 은 현재 로그인한 user의 정보를 보여준다.
  # 로그인이 되지 않은 경우는 
  # request는 요청받은 데이터 객체
  ```

  ```html
  {% user.is_authenticated %}
  ```

* 혹은 데코레이터를 사용할 수 있다.

  ```python
  from django.contrib.auth.decorators import login_required
  # ...
  @login_required
  def .....
  ```

  

## 11. 회원정보 변경

```python
# views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm

@login_required
def update(request):
    if request.method == 'POST':
        # 1. 사용자가 보낸 내용을 담아서
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # 2. 검증
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/form.html', {'form': form})

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)  # 반드시 첫번째
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})
```



## 12. User 기능

### 1. 장고 User

* 장고는 User관련 기능이 내부적으로 있어서 가져다 쓰면 된다.

* django.contrib.auth.models.User 를 변경해야 한다면

  => 상속받아서 만들면 된다.

  => DB와 연결되어 있어 다 변경해야 함

  => 프로젝트를 만들면서 미리 수행 권장 : Django 추천

  => 변경 후 settings 설정의 AUTH_USER_model()

  => User클래스는 get_user_model() settings설정에서  

  

* models.py에서 get_user_model 사용이 힘들다.

  => 장고 명령어 수행 순서 때문에 사용하지 못할 수 있다.

  => User 클래스가 아직 없을 수 있다.

  => 그냥 settings.AUTH_USER_MODEL 을 사용하면 알아서 바꿔준다.

* UserCreationForm을 못쓰는 이유

  => 실제 내부 코드는 User을 import해서 사용(from django.contrib.auth.models import User)

  => get_user_model()을 사용하고 상속받아 덮어쓰자

* 프로젝트 시작시 User 모델을 빼자

  => User 클래스가 필요하면, get_user_model()을 호출하여 사용하자.

  => models.py에서만 settings.AUTH_USER_MODEL 을 사용하자.

### 2. User객체를 저장하는 Model 설정

```python
from django.db import models
from django.conf import settings

class Article(models.Model):
    # ......
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 로그인된 User객체 저장
    # settings.AUTH_USER_Model : 'accounts.User'(str)
# from django.conf import settings.AUTH_USER_MODEL
```

`from django.conf import settings.AUTH_USER_MODEL` : 현재 로그인된 User class 객체

`from django.contrib.auth import get_user_model` : User class

## 13 .(User) Django Authentication

### `User` Class

> django에서는 프로젝트를 시작할 때, 항상 `User`Class를 직접 만드는 것을 추천함! [링크]( https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model )
>
> django의 기본 Authentication과 관련된 설정 값들을 활용하기 위해 `accounts` 앱으로 시작하는 것을 추천(ex-LOGIN_URL = '/accounts/login/')

1. `models.py`

   ```python
   # accounts/models.py
   from django.contrib.auth.models import AbstractUser
   
   class User(AbstractUser):
       pass
   ```

   > django 내부에서 `User`를 기본적으로 사용한다. ex) `python manage.py createsuperuser`
   >
   > 확장 가능성(변경)을 위해 원하는 앱에 내가 원하는 형식으로 class를 정의
   >
   > `User`상속관계 [Github 링크]( https://github.com/django/django/blob/master/django/contrib/auth/models.py#L384 )   [공식문서링크]( https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#fields )
   >
   > * `AbstractUser` : `username`, `last_name`, `first_name`, `email`, ....
   > * `AbstractBaseUser`: `password`, `last_login`
   > * `models.Model`

2. `settings.py`

   ```python
   # project/settings.py
   
   AUTH_USER_MODEL = 'accounts.User'
   ```

   * `User`클래스를 활용하는 경우에는 `get_user_model()`을 함수를 호출하여 사용한다.

     ```python
     # accounts/forms.py
     from django.contrib.auth import get_user_model
     
     class CustomUserChangeForm(UserChangeForm):
         class Meta:
             model = get_user_model() # User return
             fields = ['username', 'first_name', 'last_name']
     ```

     

   * 단, `models.py`에서 사용하는 경우에는 `settings.AUTH_USER_MODEL`을 활용한다.[settings]( https://docs.djangoproject.com/en/2.2/ref/settings/#auth-user-model )

     ```python
     # articles/models.py
     from django.conf import settings
     
     class Article(models.Model):
         user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASECADE)
     ```
     
     [공식문서-Referencing the `User`model]( https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#referencing-the-user-model)
   
3. `admin.py`

   * admin 페이지를 활용하기 위해서는 직접 작성을 해야 한다.

   * `UserAdmin`설정을 그대로 활용할 수 있다.

     ```python
     # accounts/admin.py
     from django.contrib.auth.admin import UserAdmin
     from .models import User
     
     admin.site.register(User, UserAdmin)
     ```

     

## 14. Authentication Forms

### 1. `UserCreationForm`: ModelForm

* custom user를 사용하는 경우 직접 사용할 수 없음.
  * 실제 코드상에 `User`가 직접 import 되어 있기 때문에[Github 링크]()

```python
# accounts/form
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model() # User return
        fields = ['username', 'first_name', 'last_name']
```

* `ModelForm`이므로 활용 방법은 동일하다.

### 2. `UserChangeForm`: ModelForm

* custom user를 사용하는 경우 직접 사용할 수 없음.
* 그대로 활용하는 경우 `User`와 관련된 모든 내용을 수정하게 됨
  * 실제 코드상에 필드가 `__all__`로 설정되어 있음. [Github 링크]()

```python
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')
```



### 3. `AuthenticationForm`

* `ModelForm`이 아님! **인자 순서를 반드시 기억하자**
* `AuthenticationForm(request, data, .....)`

```python
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST) # cookie와 session을 request를 통해 넘겨준다.
        if form.is_valid():
            # 로그인
            # from IPython import embed
            # embed()
            user = form.get_user() # user를 가지고 와서
            auth_login(request, user) # login함수에 입력
            return redirect(request.GET.get('next') or 'articles:index') # 단축평가
            # return redirect('articles:index')
    else:
        form = AuthenticationForm()
        print(form)
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```

* 로그인에 성공한 `user`의 인스턴스는 `get_user()`메소드를 호출하여 사용한다.

* 실제 로그인은 아래의 함수를 호출하여야 한다.

  ```python
  from django.contrib.auth import login as auth_login
  auth_login(request, user)
  ```

  

### 4. `PasswordChangeForm`

* `ModelForm`이 아님! **인자 순서를 반드시 기억하자**

* `PasswordChangeForm(user, data)`

  ```python
  if request.method == 'POST':
  	form = PasswordChangeForm(request.user, request.data)
  else:
      form = PasswordChangeForm(request.user)
  ```

* 비밀번호가 변경이 완료된 이후에는 기존 세션 인증 내역이 바뀌어서 자동으로 로그아웃된다. 따라서, 아래의 함수를 호출하면, 변경된 비밀번호로 세션 내역을 업데이트한다.

  ```python
  from django.contrib.auth import update_session_auth_hash
  update_session_auth_hash(request, form.user)
  ```

## 15. (참고사항)Appendix.import

```python
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import User
from django.contrib.auth.forms import AbstractUser
from django.contrib.auth.forms import AbstractBaseUser
from django.contrib.auth.decorators import login_required
```

```python
from django.conf import settings
```

```python
from django.db import models # models.Model, models.CharField()......
from django import forms # forms.ModelForm, forms.form
```

```python
from django.shortcuts import render, redirect, get_object_or_404
```

```python
from django.views.decorators.http import require_POST, ....
```

## 16 .M:N Many to many

### 1. 중개 모델

```python
from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()

class Patient(models.Model):
    name = models.TextField()

class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```

1. 예약 만들기

   ```python
   d1=Doctor.objects.create(name='kim')
   p1=Patient.objects.create(name='taewoo')
   Reservation.objects.create(doctor=d1,patient=p1)
   ```

2. 1번 환자의 예약 목록

   ```python
   p1.reservation_set.all()
   ```

3. 1번 의사의 예약 목록

   ```python
   d1.reservation_set.all()
   ```

4. 1번 의사의 환자 목록

   * 지금 상태에서 바로 의사가 해당하는 환자들로 접근을 할 수는 없다.

   ```python
   for r in d1.reservation_set.all():
       print(r.patient)
   ```

### 2. 중개 모델(through 옵션)

> 의사->환자 혹은 환자->의사로 접근을 하기 위해서는 `ManyToManyField`옵션을 사용한다.
>
> `Reservation`모델을 활용하려면 `through`옵션을 사용한다.
>
> `through`옵션이 없으면, 기본적으로 `APPNAME_patient_doctor` 테이블을 생성한다.

```python
from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()
    
class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor, through='Reservation')

class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```

* 마이그레이션 파일을 만들거나 마이그레이트 할 필요가 없다.
* 즉, 데이터베이스는 전혀 변경되는 것이 없다.

1. 1번 의사의 예약 목록

   ```python
   d1.reservation_set.all()
   ```

2. 1번 의사의 환자 목록

   > `Doctor`는 `Patient`의 역참조이므로, `naming convention`에 따라 아래와 같이 접근

   ```python
   d1.patient_set.all()
   ```

3. 1번 환자의 의사 목록

   * `Patient`는 `Doctor`의 직접참조(`Doctor`)이므로, 아래와 같이 접근

   ```pyhon
   p1.doctors.all()
   ```

#### 2.1 `related_name`

```python
from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()
    

class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor, through='Reservation', related_name='patients')

class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```

* 역참조시 `related_name`옵션으로 직접 설정할 수 있다.
  * 설정하지 않으면 기본적으로 `Model명_set`으로 된다.
* 반드시 설정할 필요는 없지만, 필수적인 상황이 발생할 수 있다.
  * ex) `User` - `Article`
* 따라서, `ManyToManyField`를 쓸 때에는 항상 `related_name`을 설정하고, 모델의 복수형으로 표기하자.

1. 1번 의사의 환자 목록

   ```python
   d1.patients.all()
   ```

### 3. 중개모델 없이 작성

```python
from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()
    

class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor, related_name='patients')
```

* `앱이름_patient_doctors`로 테이블이 자동으로 생성된다.
* 별도의 컬럼이 필요 없는 경우는 위와 같이 작성한다.
* 만약, 예약시 추가정보(ex - 시간, 담당자 ....)를 담기 위해서라면 반드시 중개 모델이 필요하다.

1. 예약 생성

   ```python
   d2 = Doctor.objects.create(name='kim')
   p2 = Patient.objects.create(name='hwang')
   
   d2.patients.add(p2)
   ```

2. 예약 취소

   ```python
   d2.patients.remove(p2)
   ```

## 17. 좋아요 구현

```python
user.like_articles.all()  # related_name (M2M)
# => Queryset (article instance 담겨있음)
user.article_set.all()  # related_name X (FK 1:N)
# => Queryset (article instance 담겨있음)
article.user  # FK(1:N)
# => article을 작성한 user instance
article.like_users.all() # M2M
# => Queryset article에 좋아요를 한 
```

```html
{{article.like_user.count}}
댓글수 {{article.comment_set.all()}}
```



