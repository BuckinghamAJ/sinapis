from django.shortcuts import render
from .forms import PostForm
from .models import Post



# Create your views here.

def get_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        post = None
    
    if post:
        context = {
            'post': post,
        }
        return render(request, 'posts/post_modal.html', context=context)

def submit_new_post(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.save()

    return render(request, 'posts/new_post.html#post-form')