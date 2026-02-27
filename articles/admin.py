from django.contrib import admin
from .models import Article, Category, Tag

# Register your models here.
@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')  # 后台列表显示字段
    list_filter = ('status', 'category')    # 右侧过滤器
    search_fields = ('title', 'content')    # 搜索字段
    ordering = ('-created_at', )    # 默认排序



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')



@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')



