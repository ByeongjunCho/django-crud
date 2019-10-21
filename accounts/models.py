from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):  # 확장 가능성을 위해 직접 만들어서 사용 권장
    pass