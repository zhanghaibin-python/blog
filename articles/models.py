from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from pypinyin import lazy_pinyin
import uuid


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="分类名称")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL标识")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # 先将name转换为拼音，在把 name_pinyin 转换成 URL Friendly 的 slug 标识
            name_pinyin = '-'.join(lazy_pinyin(self.name))
            self.slug = slugify(name_pinyin)
            if Category.objects.filter(slug=self.slug).exists():
                self.slug = f'{self.slug}-{uuid.uuid4().hex[:4]}'
        super().save(*args, **kwargs)   # 调用原来的 save  方法， 保存到数据库



class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name="标签名称")


    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Article(models.Model):

    STATUS_CHOICES = (
    ('draft', '草稿'),
    ('published', '已发布')
    )

    title = models.CharField(max_length=150, verbose_name="标题")
    content = models.TextField(verbose_name="文章正文")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", verbose_name="作者")
    # 采用 models.PROTECT 确保文章分类不可删除，
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="articles", verbose_name="分类")
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles", verbose_name="标签")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft", verbose_name="状态")
    views = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")


    class Meta:
        ordering = ['-created_at']
        verbose_name = "文章"
        verbose_name_plural = "文章"


    def __str__(self):
        return self.title



