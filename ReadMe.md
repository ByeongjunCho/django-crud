# Django - CRUD

> Django ORM을 활용하여 게시판 기능 구현하기

# 1. 환경설정

* 가상환경(venv)

  * python 3.7.4

* pip - `requirements.txt`확인

  * 현재 패키지 리스트 작성

    ```bash
    $ pip freeze > requirements.txt
    ```

  * 만약, 다른 환경에서 동일하게 설치한다면

    ```bash
    $ pip install -r requirements.txt
    ```

* django app -`articles`

# 2. Model 설정

## 1. `Article` 모델 정의

```python
# articles/models.py

class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    # DateTimeField
    #    auto_now_add : 생성시 자동으로 입력
    #    auto_now : 수정시마다 자동으로 기록
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

* 클래스 정의할 때는 `models.Model`을 상속받아 만든다.

* 정의하는 변수는 실제 데이터베이스에서 각각의 필드(column)을 가지게 된다.

* 주요 필드

  * `CharField(max_length)`

    * 필수 인자로 `max_length`를 지정하여야 한다.
    * 일반적으로 데이터베이스에서 `VARCHAR`로 지정된다.
    * `<input type="text">`

  * `TextField()`

    * 일반적으로 데이터베이스에서 `TEXT`으로 지정된다.
    * `CharField`보다 더 많은 글자를 저장할 때 사용된다.
    * `<textarea>`

  * `DateTimeField()`

    * 파이썬의 datetime 객체로 활용된다.
    * 옵션
      * `auto_now_add=True`: 생성시에 자동으로 저장(게시글 작성일)
      * `auto_now=True`: 변경시에 자동으로 저장(게시글 수정일)
    * `BooleanField()`, `FileField()`, `IntegerField()` 등 다양한 필드를 지정할 수 있다.

  * `id`값은 자동으로 `INTEGER`타입으로 필드가 생성되고, 이는 `PK(Primary Key)` 이다.

  * 모든 필드는 `NOT NULL`조건이 선언되며, 해당 옵션을 수정하려면 아래와 같이 정의할 수 있다.

    ```python
    username = models.CharField(max_length=10, nullable=True)
    ```

## 2.  마이그레이션(migration)파일 생성

> 마이그레이션(migration)은 모델에 정의한 내용(데이터베이스의 스키마)의 변경사항을 관리한다. 

따라서, 모델의 필드 수정 혹은 삭제 등이 변경될 때마다 마이그레이션 파일을 생성하고 이를 반영하는 형식으로 작업한다.

```bash
$ python manage.py makemigrations
Migrations for 'articles':
  articles\migrations\0001_initial.py
    - Create model Article
```

* 만약, 현재 데이터베이스에 반영되어  있는 마이그레이션을 확인하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py showmigrations
  [ ] 0001_initial
  [ ] 0002_logentry_remove_auto_add
  ....
  ```

  

## 3. DB 반영(migrate)

> 만들어진 마이그레이션 파일을 실제 데이터베이스에 반영한다.

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, articles, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  ......
```

* 만약 특정 app의 마이그레이션 혹은 특정 버전만 반영하고 싶다면 아래의 명령어를 활용한다.

  ```bash
  $ python manage.py migration articles
  $ python manage.py migration articles 0001
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

* 데이터베이스에 테이블을 만들 때, 기본적으로 `app이름_model이름`으로 생성된다.

# 3. Django Query Methods

> Django ORM을 활용하게 되면, 파이썬 객체 조작으로 데이터베이스 조작이 가능하다.
>
> ORM(Object-Relational-Mapping)에서는 주로 활용되는 쿼리문들이 모두 method로 구성되어 있다.

```bash
$ python manage.py shell
$ python manage.py shell_plus
```

* `shell`에서는 내가 활용할 모델을 직접 `import`해야 한다.

  ```python
  from articles.models import Article
  ```

  

* `shell_plus`는 `django_extensions`를 설치 후 `INSTALLED_APPS`에 등록하고 활용해야 한다.

  ```bash
  $ pip install django-extensions
  ```

  ```python
  # crud/setting.py
  INSTALLED_APPS = [
      'django_extensions',
      ...
  ]
  ```

  

## 1. Create

```python
# 1. 인스턴스 생성 및 저장
article = Article()
article.title = '1번글'
article.content = '1번내용'
article.save()
# article = Article(title='글', content = '내용')
# article.save()

# 2. create 메서드 활용
article = Article.objects.create(title='글', content='내용')
```

* 데이터베이스에 저장되면, `id`값이 자동으로 부여된다. `.save()`호출하기 전에는 `None`이다.

## 2. Read

* 모든 데이터 조회

  ```python
  Article.objects.all()
  ```

  * 리턴되는 값은 `QuerySet`오브젝트
  * 각 게시글 인스턴스들을 원소로 가지고 있다.

* 특정(단일) 데이터 조회

  ```python
  Article.objects.get(pk=1)
  ```

  * 리턴되는 값은 `Article`인스턴스
  * `.get()`은 그 결과가 여러개 이거나 없는 경우 오류를 발생시킴.
  * 따라서, 단일 데이터 조회시(primary key를 통해)에만 사용한다.

* 특정 데이터 조회

  ```python
  Article.objects.filter(title='제목1')
  Article.objects.filter(title__contains='제목') # '제목'이 들어간 모든 데이터
  Article.objects.filter(title__startswith='제목') # '제목'으로 시작하는 제목
  Article.objects.filter(title__endswith='제목') # '제목'으로 끝나는 제목
  ```

  * 리턴되는 값은 `QuerySet`오브젝트
  * `.filter()`는 없는 경우/하나인 경우/여러개인 경우 모두 `QuerySet`리턴

## 3. Update

```python
article = Article.objects.get(pk=1)
article.content = '내용 수정'
article.save()
```

* 수정은 특정 게시글을 데이터베이스에서 가져와서 인스턴스 자체를 수정한 후 `save` 호출

## 4. Delete

```python
article = Article.objects.get(pk=1)
article.delete()
```

## 5. 기타

### 1. Limiting

```python
Article.objects.all()[0] # LIMIT 1 : 1개만
Article.objects.all()[2] # LIMIT 1 OFFSET 2
Article.objects.all()[:3]
```

### 2. Ordering

```python
Article.objects.order_by('-id') # id 기준으로 내림차순 정렬
Article.objects.order_by('title') # title을 기준으로 오름차순 정렬
```

# 실습 - 게시판 CRUD

> 보통 순서는 Model 작성 후 urls.py -> views.py -> Template__.html 작성 순으로 이루어진다.

## 1. Create

```python
# urls.py
from . import views
urlpatterns = [
    # ....
    path('new/', views.new),
    # ....
]

# views.py
# ...
def new(request):
    
    return render(request, 'articles/new.html')
# ....
```

```html
<!-- new.html -->
<form action="/articles/create/">
  <div class="form-group">
    <label for="exampleInputEmail1">제목</label>
    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="제목">
    <small id="emailHelp" class="form-text text-muted">글의 제목을 작성해주세요</small>
  </div>
  <div class="form-group">
    <label for="exampleFormControlTextarea1">내용</label>
    <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

* 새로운 데이터베이스를 생성하기 위해 `form`이 있는 html파일을 생성한다.
* 여기서 입력된 값을 `action="/articles/create/"`으로 보낸다.

```python
# urls.py
from . import views
urlpatterns = [
    # ....
    path('create/', views.create),
    # ....
]

# views.py
# ...
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
# ....
```

* 입력되는 값 title과 content를 Article객체를 이용하여 데이터베이스에 생성한다.

## 2. Read

```python
# urls.py
from . import views
urlpatterns = [
    # ....
    path('<int:article_pk>/', views.detail),
    # ....
]

# views.py
# ...
def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)
# ....
```

```html
<h1>{{article.id}}번 글</h1>
<h2>제목: {{article.title}}</h2>
<p>작성일자 : {{article.created_at}}</p>
<p>수정일자 : {{article.updated_at}}</p>
<hr>
<p>작성내용 : {{article.content}}</p>
<a href="/articles/" class="btn btn-info">목록으로</a>
<a href="/articles/{{ article.pk }}/delete/" class="btn btn-warning">글 삭제하기</a>
<a href="/articles/{{ article.pk }}/edit/"class="btn btn-primary">수정하기</a>
```

* url에서 입력된 interger값을 Key로 사용하여 해당 key에 대응되는 데이터베이스 객체를 html파일에 넘겨준다.

## 3. Update

```python
# urls.py
from . import views
urlpatterns = [
    # ....
    path('<int:article_pk>/edit/', views.edit),
    path('<int:article_pk>/update/', views.update),
    # ....
]
# views.py
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
```

* 생성과 비슷하게 편집 가능한 Templates를 만들고, 여기서 수정된 값을 update url로 보내서 데이터를 수정한다.

## 4. Delete

```python
# urls.py
from . import views
urlpatterns = [
    # ....
    path('<int:article_pk>/delete/', views.delete),
    # ....
]
# views.py
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()
    return redirect('/articles/')
```

* key를 입력받아 데이터베이스에 접근하여 해당 key에 관한 데이터를 삭제한다.



## 참고

> 작성순서는 초기 모델설정-> url.py -> views.py -> templates/___.html 순이다. (Model->View->Templates)

# 정리

사용자  -----------------------------------------------------------------------------------------------------------> django

​																															view                                   model

​															urls.py - /articles/new/		----->			form  									db

​																										<------          form(requests.GET(....))																																									class Article



![img](data:image/png;base64,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z3e33nqre/rpp6OLrRCD2+67kDFQBgKpE0Akp+5hxgcBCBQSSEGkDBqDhOadd97p3n77bXfaaae5q6++eorgfPTRR92GDRvcK6+84vTvl156KeN07bXX9srp9/vuuy9LlXjqqad6KRx+3e985zvuiiuucB988IF79tlnp6RVFIlk2aX66veTTz5xl1xyifvRj37krrvuuixvWX978MEH3YEDB9z06dMz21X2ggsuyOzTivqaNWvcm2++6ebOnetuvvlmt27duuiiPIX4iw46BkOgJAFEcklgFIcABNIgkIJI6TcGpSp89NFHPZH52WefucOHD7vZs2e7/fv3Zw40AavfJEjPPPPMrI6ORYsWZeJa9XSo7oknnuiOHDkype65557r9u7d60455RT3xRdfuKNHj2bt/PWvf80Eb5FInjFjRtaeyp199tlu586dWZsbN27MUitJVB5IAAASZElEQVRMmKuML5IlxlVHtsrmWbNmZSJbfS5YsMDt2LEjqsBMIf6iAo6xEBiBACJ5BGhUgQAE4ieQgkgpGoOlKkhISvRKrH711Vfu4osvdnv27HFbtmxxS5Ys6QlYCdE//elP2Uqtn/fspzqY6H733XezciZ+VXfbtm3Z6rFeLFQf6tNyovMi+d5773Xr16+fImplmwSvBPC+ffumiHDfhq1bt7qlS5ceV9eEs9kWS2SmEH+xsMZOCIxKAJE8KjnqQQACURNIQaQUjaFfHnBeZFq5/CqstSmxaztkWNlVq1ZlqQ3231pJ3r17dy8OtAq8YsWKXi5xaE7ytGnTshXhY8eO9RXJl156abbq7Nulwvk+YwnKFOIvFtbYCYFRCSCSRyVHPQhAIGoCKYiUojHMmTOnlz7hO+jgwYO937ViawLW0hysrNrUCvGhQ4d61a2srezm/9sK2kq0iecikWz5zKpjaSBWf5BI9tM0isalFBGtasdypBB/sbDGTgiMSgCRPCo56kEAAlETSEGkFI3BVmUtbzfvpIsuuigTk/1WedWmn/qg+v1Ecl5gm0i2+vk+7L/VpkTt6aefnv1PLxAOW0m2sartosPGFUtQphB/sbDGTgiMSgCRPCo56kEAAlETSEGkFI3B8oct97ifkwatJIeK5PzqraV05FecLUfZVoP9FA/lMpvwDVlJji33uB//FOIv6gsAxkMggAAiOQASRSAAgfQIpCBS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)



```python
# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),  # articles app/urls.py의 모든 path에 default로 /articles/를 붙인다.
]
```





```python
# 생성
article = Article()
article.title = '제목'
article.content = '컨텐트'
article.save()

# 내용 변경
article.title = '수정제목'
article.content = '수정컨텐트'
article.save()  # 수정된 내용 저장

# 내용 접근
Article.objects.get(id=1)  # 하나의 값만 리턴
Article.objects.get(title='__제목__') # 여러개 리턴 불가(1개는 가능하지만 여러개가 있을 수 있음)
Article.objects.filter(title='__제목__')  # 여러개의 값 리턴 가능
Article.objects.all().first() # 처음값
Article.objects.all().last() # 마지막값
# 특정 언어가 있는 값
Article.objects.filter(title__contains='__원하는값__')
Article.objects.filter(content__contains='__원하는값__')
Article.objects.filter(content__startswith='__원하는값__') # 시작이 __원하는값__을 찾음
Article.objects.filter(content__endswith='__원하는값__') # 끝이 __원하는값__을 찾음

```
