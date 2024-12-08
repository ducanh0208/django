from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from comment.models import Comment
from comment.forms import CommentForm
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required

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
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()

        else:
            form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("Bài viết không tồn tại")

    return render(request, 'post.html', {
            'post': post, 
            'comments': comments,
            'form': form,
        }
    )

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all()
    form = CommentForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

# View to edit a comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Ensure the current user is the author of the comment
    if comment.author != request.user:
        raise Http404("You are not authorized to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {'form': form})

# View to delete a comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Ensure the current user is the author of the comment
    if comment.author != request.user:
        raise Http404("You are not authorized to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    
    return render(request, 'blog/delete_comment.html', {'comment': comment})
