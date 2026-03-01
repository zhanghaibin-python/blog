from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Article, Category
from django_redis import get_redis_connection
from django.core.cache import cache


class ArticleTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Django')
        self.list_url = reverse('articles')

        # 清理 Redis，防止之前的测试残留
        get_redis_connection("default").flushdb()

    def test_create_article(self):
        """测试发布文章"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Article',
            'content': 'Content',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)

    def test_create_article_unauthorized(self):
        """测试未登录发布"""
        data = {'title': 'Fail', 'content': 'Content', 'category': self.category.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_counter(self):
        """测试阅读量 Redis 计数"""
        # 1. 准备数据
        article = Article.objects.create(
            title='Hot Article',
            content='Content',
            author=self.user,
            category=self.category,
            status='published',
            views=0
        )
        url = reverse('article_detail', args=[article.id])

        # 2. 模拟访问
        self.client.get(url)  # 第一次访问
        self.client.get(url)  # 第二次访问

        # 3. 验证 Redis 里的值
        redis_conn = get_redis_connection("default")
        key = f"article:views:{article.id}"
        incr = int(redis_conn.get(key))

        self.assertEqual(incr, 2, "Redis 中的计数应该是 2")

        # 4. 验证数据库里的值（应该还是 0，因为还没同步）
        article.refresh_from_db()
        self.assertEqual(article.views, 0, "数据库里的值应该还没变")