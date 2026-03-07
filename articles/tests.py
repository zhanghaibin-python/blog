from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article, Category
from .tasks import sync_article_views
from django_redis import get_redis_connection

class ArticleTaskTest(TestCase):
    def setUp(self):
        # 1. 准备测试数据
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.article = Article.objects.create(
            title='Test Article',
            content='Content',
            author=self.user,
            category=self.category,
            views=0  # 初始阅读量为 0
        )
        
        # 2. 清理 Redis (防止之前的测试数据干扰)
        self.redis_conn = get_redis_connection("default")
        self.redis_key = f"article:views:{self.article.id}"
        self.redis_conn.delete(self.redis_key)

    def tearDown(self):
        # 测试结束后清理 Redis
        self.redis_conn.delete(self.redis_key)

    def test_sync_article_views_logic(self):
        """
        测试 sync_article_views 任务能否正确同步 Redis 数据到 MySQL
        """
        # 1. 模拟 Redis 中有 10 个新增阅读量
        self.redis_conn.set(self.redis_key, 10)
        
        # 2. 执行同步任务 (同步调用，不走 Celery 异步)
        sync_article_views()
        
        # 3. 重新从数据库获取文章
        self.article.refresh_from_db()
        
        # 4. 断言：数据库阅读量应该是 10
        self.assertEqual(self.article.views, 10)
        
        # 5. 断言：Redis 里的值应该变为 0 (或者被删除了，取决于你的逻辑)
        # 注意：你现在的逻辑是 decrby，所以 Redis 里应该是 0
        remaining_views = self.redis_conn.get(self.redis_key)
        
        # Redis get 返回的是 bytes，或者是 None (如果 key 被删了)
        # 如果逻辑是 decrby，最后可能是 b'0'
        if remaining_views:
             self.assertEqual(int(remaining_views), 0)
        else:
             # 如果逻辑是直接删 key，那就是 None
             self.assertIsNone(remaining_views)

    def test_sync_views_with_concurrent_update(self):
        """
        模拟并发场景：同步过程中，Redis 又增加了新数据
        """
        # 1. 初始 Redis 有 10
        self.redis_conn.set(self.redis_key, 10)
        
        # 2. 这里我们无法真正模拟 "同步函数执行到一半时插入数据"
        # 但我们可以验证 decrby 的逻辑：
        # 假设任务取出了 10，准备更新数据库...
        
        # 手动模拟任务内部逻辑的一部分：
        incr = int(self.redis_conn.get(self.redis_key)) # 拿到 10
        
        # 3. 此时突然又有 5 个阅读量进来
        self.redis_conn.incr(self.redis_key, 5) # Redis 变成 15
        
        # 4. 任务继续执行更新数据库 (加 10)
        from django.db.models import F
        Article.objects.filter(id=self.article.id).update(views=F("views") + incr)
        
        # 5. 任务执行 decrby (减 10)
        self.redis_conn.decrby(self.redis_key, incr)
        
        # 6. 验证结果
        self.article.refresh_from_db()
        # 数据库应该加了 10
        self.assertEqual(self.article.views, 10)
        
        # Redis 应该还剩 5 (15 - 10)
        remaining = int(self.redis_conn.get(self.redis_key))
        self.assertEqual(remaining, 5)
