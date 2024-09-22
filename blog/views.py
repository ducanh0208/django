from django.shortcuts import render
from .models import Post
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Post

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    
class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = '__all__'
# Create your views here.
def list(request):
   Data = {'Posts': Post.objects.all().order_by('-date')}
   return render(request, 'blog.html', Data)

def post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise Http404("Bài viết không tồn tại")

    return render(request, 'post.html', {'post': post})
