from .serializers import CategorySerializer, ArticleReadSerializer, ArticleWriteSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Article, Category
from .permissions import IsAuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from django.db.models import F
from django.core.cache import cache
from rest_framework.response import Response
# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    """
    定义分页器
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleListCreateAPIView(ListCreateAPIView):
     """
     继承 ListCreateAPIView 自动处理
     get(list) 和 post(create)
     """
     permission_classes = [IsAuthenticated]
     # 显示挂载分页器
     pagination_class = StandardResultsSetPagination

     def get_queryset(self):
         # 保持你原有得查询优化
         return Article.objects.filter(status="published").select_related("author", "category").prefetch_related("tags")

     def get_serializer_class(self):
         # 动态选择序列器
         if self.request.method == "POST":
             return ArticleWriteSerializer
         return ArticleReadSerializer

     def perform_create(self, serializer):
         # 自关联当前用户
         serializer.save(author=self.request.user)


class ArticleDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    GET: 获取文章详情（含缓存 + 阅读量）
    PUT: 全量更新文章
    PATCH: 部分更新
    DELETE: 删除文章
    """
    # 加上 select_related('author')，一次查询搞定对象获取和权限校验
    queryset = Article.objects.select_related('author').all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        """
        动态选择 serializer
        """
        if self.request.method in ['PUT', 'PATCH']:
            return ArticleWriteSerializer
        return ArticleReadSerializer

    # ====== 详情读取（缓存 + 阅读量）======
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 使用 F 表达式直接更新数据库，不经过 Python 内存对象，原子操作
        # 注意：因为频繁更新数据库会影响性能，高并发下通常先写 Redis 计数，在定时同步到 MySQL
        instance.views = F('views') + 1
        instance.save(update_fields=['views'])
        # 刷新实例以获取最新 views 值（因为 F 表达式执行后 instance 内存值未变）
        instance.refresh_from_db()

        # 定义缓存 Key, 例如：article_detail_12
        cache_key = f'article_detail_{instance.id}'
        # 尝试从缓存获取数据
        data = cache.get(cache_key)

        if not data:
            # 缓存未命中：序列化并写入缓存
            serializer = self.get_serializer(instance)
            data = serializer.data
            # 设置过期时间 60 * 15 秒（15分钟），防止缓存雪崩
            cache.set(cache_key, data, 60 * 15)
        else:
            # 缓存命中：直接使用，但由于我们刚更新了 views，需要手动更新缓存中得 views 字段
            # 这是一个权衡：为了性能，我们可以允许缓存中的 views 稍微滞后， 或者手动 patch 一下
            data['views'] = instance.views

        return Response(data)


class CategoryListAPIView(ListAPIView):
    """
    get: 获取分类列表
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer




