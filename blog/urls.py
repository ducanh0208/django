from django.urls import path
from . import views
from .views import BlogListView, BlogDetailView, BlogCreateView

urlpatterns = [
   path('', views.list, name='blog'),
   path('<int:id>/', views.post, name='post'),
   path('post/<int:id>/', views.post, name='post'),
   path('post/new/', BlogCreateView.as_view(), name='post_new'),
   path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
   path('', BlogListView.as_view(), name='home'),
   path('post/<int:pk>/', views.post_detail, name='post_detail'),  # View the post and its comments
   path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),  # Edit comment
   path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),  # Delete comment
]
