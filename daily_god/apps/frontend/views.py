from django.shortcuts import render
from posts.models import Post
from quotes.models import Quote
from prayers.models import Prayer

from itertools import chain
# Create your views here.

def home(request):

    try:
        latest_posts = Post.objects.order_by('-created_at')[:50]
    except Post.DoesNotExist:
        latest_posts = []

    try:
        latest_quotes = Quote.objects.order_by('-created_at')[:50]
    except Quote.DoesNotExist:
        latest_quotes = []

    try:
        latest_prayers = Prayer.objects.order_by('-created_at')[:50]
    except Prayer.DoesNotExist:
        latest_prayers = []

    content = [c for c in chain(latest_posts, latest_quotes, latest_prayers) if c]

    context = {
        'content': content
    }

    return render(request, 'index.html', context=context)