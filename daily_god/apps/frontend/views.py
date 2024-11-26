from django.shortcuts import render
from posts.models import Post
from posts.forms import PostForm
from quotes.models import Quote
from prayers.models import Prayer


from itertools import chain
# Create your views here.

def home(request):

    post_form = PostForm()

    try:
        latest_posts = Post.objects.filter(is_approved=True).order_by('-created_at')[:50]
    except Post.DoesNotExist:
        latest_posts = []

    try:
        latest_quotes = Quote.objects.filter(is_approved=True).order_by('-created_at')[:50]
    except Quote.DoesNotExist:
        latest_quotes = []

    try:
        latest_prayers = Prayer.objects.filter(is_approved=True).order_by('-created_at')[:50]
    except Prayer.DoesNotExist:
        latest_prayers = []

    content = [c for c in chain(latest_posts, latest_quotes, latest_prayers) if c]

    context = {
        'content': content,
        'post_form': post_form,
    }

    return render(request, 'index.html', context=context)




def get_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        post = None
    
    if post:
        context = {
            'post': post,
        }
        return render(request, 'components/post_modal.html', context=context)


    return 
