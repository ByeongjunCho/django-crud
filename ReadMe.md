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
        comment = comment_form.save(commit=False)  # comment object
        comment.article = article
        comment.save()
        # 4. return redirect
        return redirect('articles:detail', article_pk)
```





