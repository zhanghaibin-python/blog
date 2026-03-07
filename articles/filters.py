import django_filters
from .models import Tag, Article

class ArticleFilter(django_filters.FilterSet):
    # icontains: 不区分大小写的包含关系
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    # 精确匹配分类
    category = django_filters.NumberFilter(field_name='category')
    # 标签过滤（多对多）
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags__name', to_field_name='name', queryset=Tag
                                                     .objects.all().distinct())
    
    class Meta:
        models = Article
        fields = ['title', 'category', 'tags']