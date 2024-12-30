from django.shortcuts import render
from .forms import PostForm
from .models import Post
from django.http import HttpResponse
from comments.forms import SeedCommentForm
from django.core.cache import cache


# Create your views here.

def get_post(request, id):
    post = cache.get(f'post_{id}')
    if not post:
        try:
            post = Post.objects.get(id=id)
            cache.set(f'post_{id}', post)
        except Post.DoesNotExist:
            post = None
    
    if post:
        context = {
            'content': post,
            'type': 'post',
        }
        return render(request, 'components/modal.html', context=context)
    
    return None

def submit_new_post(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.save()

    return render(request, 'posts/new_post.html#post-form')