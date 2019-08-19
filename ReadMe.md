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



### 

ORM(Object Relational Mapping) : python과 SQL간을 객체로 연동해주는 방법



