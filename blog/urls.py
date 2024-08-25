from django.urls import path
from . import views
from .views import BlogListView,BlogDetailView, BlogCreatView

urlpatterns = [
   path('', views.list, name='blog'),
   path('<int:id>/', views.post, name='post'),
   path('post/new/', BlogCreatView.as_view(), name='post_new'),
   path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
   path('', BlogListView.as_view(), name='home'),
]

