from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class User(AbstractUser):  # 확장 가능성을 위해 직접 만들어서 사용 권장
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)