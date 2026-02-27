from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=10, verbose_name="名称", default='', blank=True)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True, verbose_name="头像")
    bio = models.TextField(max_length=200, blank=True, null=True, verbose_name="简介")
