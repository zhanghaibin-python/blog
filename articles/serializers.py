from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# 拆分 read/write serializer
class ArticleReadSerializer(serializers.ModelSerializer):
    """
    定义读取serializer
    """
    # 将 关联 category 对象序列化为字典
    category = CategorySerializer(read_only=True)
    # 将关联得标签 tags 改为字符串列表
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'category',
            'tags',
            'views',
            'created_at'
        ]



class ArticleWriteSerializer(serializers.ModelSerializer):
    """
    用于写入的serializer
    """
    class Meta:
        model = Article
        fields = [
            'title',
            'category',
            'tags',
            'content',
            'status'
                  ]







