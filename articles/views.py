from .serializers import CategorySerializer, ArticleReadSerializer, ArticleWriteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Article, Category
from .permissions import IsAuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from django.core.cache import cache
from rest_framework.response import Response
from django_redis import get_redis_connection
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
    # 组合权限：
    # 1. IsAuthenticatedOrReadOnly: 未登录只能 GET，登录了才能 PUT/DELETE
    # 2. IsAuthorOrReadOnly: 即使登录了，也必须是作者本人才能改
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

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
        redis_conn = get_redis_connection('default')
        redis_key = f"article:views:{instance.id}"
        # 只对 redis 做自增, 同时获取自增后的新值
        incr = redis_conn.incr(redis_key)
        # 设置过期时间
        redis_conn.expire(redis_key, 60 * 60 * 24)
        # 计算真实阅读量（数据库值 + Redis 增量）
        real_views = instance.views + incr
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

        response_data = data.copy()
        response_data['views'] = real_views
        return Response(data)


class CategoryListAPIView(ListAPIView):
    """
    get: 获取分类列表
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer




