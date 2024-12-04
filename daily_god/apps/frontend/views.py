from django.shortcuts import render
from posts.models import Post
from posts.forms import PostForm
from quotes.models import Quote
from prayers.models import Prayer
from itertools import chain

from django.contrib.auth import logout
# Create your views here.

def home(request):

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
    }

    return render(request, 'index.html', context=context) 





def profile_logout(request):
    logout(request)

    return render(request, 'components/topbar.html')