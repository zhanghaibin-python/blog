from django.urls import path
from .views import ArticleListCreateAPIView, ArticleDetailUpdateDestroyView, CategoryListAPIView


urlpatterns = [
    path('articles/', ArticleListCreateAPIView.as_view(), name="articles"),
    path('articles/<int:pk>/', ArticleDetailUpdateDestroyView.as_view(), name="article_detail"),
    path('category/', CategoryListAPIView.as_view(), name="category_list"),
]