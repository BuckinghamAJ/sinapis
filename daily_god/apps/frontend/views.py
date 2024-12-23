from django.shortcuts import render
from django.http import HttpResponse


from posts.models import Post
from posts.forms import PostForm
from quotes.models import Quote
from prayers.models import Prayer
from itertools import chain



import django_comments
from django_comments import signals

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
        'user': request.user,
    }

    return render(request, 'index.html', context=context) 

def bookmarked(request):
    try:
        bookmarked_posts = Post.objects.filter(bookmarked_by=request.user)
    except Post.DoesNotExist:
        bookmarked_posts = []

    try:
        bookmarked_quotes = Quote.objects.filter(bookmarked_by=request.user)
    except Quote.DoesNotExist:
        bookmarked_quotes = []

    try:
        bookmarked_prayers = Prayer.objects.filter(bookmarked_by=request.user)
    except Prayer.DoesNotExist:
        bookmarked_prayers = []

    bookmarked_content = [c for c in chain(bookmarked_posts, bookmarked_quotes, bookmarked_prayers) if c]

    context = {
        'content': bookmarked_content,
        'user': request.user,
    }

    return render(request, 'index.html', context=context)

def love_content(request, type, id):
    try:
        if type == 'post':
            content = Post.objects.get(id=id)
            context = {'post': content}
            template = 'posts/post_content.html'
        elif type == 'quote':
            content = Quote.objects.get(id=id)
            context = {'quote': content}
            template = 'quotes/quote_content.html'
        elif type == 'prayer':
            content = Prayer.objects.get(id=id)
            context = {'prayer': content}
            template = 'prayers/prayer_content.html'
    except Post.DoesNotExist or Quote.DoesNotExist or Prayer.DoesNotExist:
        content = None

    if content and request.user not in content.loved_by.all():
        content.loved_by.add(request.user)
        content.loves += 1
        content.save()
    else:
        content.loved_by.remove(request.user)
        content.loves -= 1
        content.save()

    context.update({'user': request.user})

    return render(request, template, context=context)

def bookmark_content(request, type, id):
    try:
        if type == 'post':
            content = Post.objects.get(id=id)
            context = {'post': content}
            template = 'posts/post_content.html'
        elif type == 'quote':
            content = Quote.objects.get(id=id)
            context = {'quote': content}
            template = 'quotes/quote_content.html'
        elif type == 'prayer':
            content = Prayer.objects.get(id=id)
            context = {'prayer': content}
            template = 'prayers/prayer_content.html'
    except Post.DoesNotExist or Quote.DoesNotExist or Prayer.DoesNotExist:
        content = None

    if content and request.user not in content.bookmarked_by.all():
        content.bookmarked_by.add(request.user)
    else:
        content.bookmarked_by.remove(request.user)

    context.update({'user': request.user})

    return render(request, template, context=context)

