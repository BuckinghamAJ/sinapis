from django.shortcuts import render
from django.http import HttpResponse

from posts.models import Post
from posts.forms import PostForm
from quotes.models import Quote
from prayers.models import Prayer
from itertools import chain

from .functions import love_content_by, bookmark_content_by

import django_comments
from django_comments import signals

# Create your views here.

def home(request):
    
    latest_posts = Post.objects.filter(is_approved=True).select_related('posted_by').prefetch_related('tags').order_by('-created_at')[:50]
    latest_quotes = Quote.objects.filter(is_approved=True).select_related('posted_by').prefetch_related('tags').order_by('-created_at')[:50]
    latest_prayers = Prayer.objects.filter(is_approved=True).select_related('posted_by').prefetch_related('tags').order_by('-created_at')[:50]

    content = list(chain(latest_posts, latest_quotes, latest_prayers))

    context = {
        'content': content,
    }

    return render(request, 'index.html', context)

def bookmarked(request):
    
    bookmarked_posts = Post.objects.filter(bookmarked_by=request.user).select_related('posted_by').prefetch_related('tags')
    bookmarked_quotes = Quote.objects.filter(bookmarked_by=request.user).select_related('posted_by').prefetch_related('tags')
    bookmarked_prayers = Prayer.objects.filter(bookmarked_by=request.user).select_related('posted_by').prefetch_related('tags')

    bookmarked_content = list(chain(bookmarked_posts, bookmarked_quotes, bookmarked_prayers))

    context = {
        'content': bookmarked_content,
        'user': request.user,
    }

    return render(request, 'index.html', context=context)

def love_content(request, type, id):
    context, template = love_content_by(request, type, id)
    print(context)
    if request.method == 'POST':
        component = request.POST.get('component')
        match component:
            case 'modal_heart_button':
                context = {'content': context.get('post') or 
                           context.get('quote') or 
                           context.get('prayer'), 
                           'type': type}
                template = 'components/modal.html#heart-button'
    
    return render(request, template, context=context)

def bookmark_content(request, type, id):
    context, template = bookmark_content_by(request, type, id)

    if request.method == 'POST':
        component = request.POST.get('component')
        match component:
            case 'modal_bookmark_button':
                context = {'content': context.get('post') or 
                           context.get('quote') or 
                           context.get('prayer'),
                           'type': type}
                template = 'components/modal.html#bookmark-button'

    return render(request, template, context=context)

