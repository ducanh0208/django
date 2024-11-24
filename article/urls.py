from django.urls import path
from .views import ArticleListView
from .views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDetailView,
    ArticleDeleteView,
    ArticleCreatView
)

urlpatterns = [
    path('',ArticleListView.as_view(),name='article_list'),
    path('<int:pk>/edit/',
         ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/',
         ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/',
         ArticleDeleteView.as_view(), name='article_delete'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('new/', ArticleCreatView.as_view(), name='article_new'),
]
