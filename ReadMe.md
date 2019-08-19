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
  * 따라서, 단일 데이터 조회시에만 사용한다.



### pip 설치 파일  관리

```bash
$ pip freeze > requirements.txt
```

### pip 환경 설치

```bash
$ pip install -r requirements.txt
```



## 데이터베이스

* models.py(스키마)

  ```python
  from django.db import models
  
  # Create your models here.
  # 1. 모델(스키마) 정의
  # 데이터베이스 테이블을 정의하고,
  # 각각의 컬럼(필드) 정의
  class Article(models.Model):
      # CharField - 필수인자로 max_length 지정
      title = models.CharField(max_length=10)
      content = models.TextField()
      # DateTimeField
      #    auto_now_add : 생성시 자동으로 입력
      #    auto_now : 수정시마다 자동으로 기록
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  ```

* makemigrations (마이그레이션 파일 생성)

  ```bash
  $ python manage.py makemigrations
  ```

* migrate (db 반영)

  ```bash
  $ python manage.py migrate
  ```

* ipython을 이용한 ORM

  ```bash
  $ python manage.py shell
  ```

  

### python을 이용한 SQL 조작

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



ORM(Object Relational Mapping) : python과 SQL간을 객체로 연동해주는 방법

```bash
$ pip install django-extension
$ python manage.py shell_plus
```

