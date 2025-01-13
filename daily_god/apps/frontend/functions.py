from posts.models import Post
from posts.forms import PostForm
from quotes.models import Quote
from prayers.models import Prayer
from itertools import chain
import re

def home_query():
    latest_posts = Post.objects.filter(is_approved=True).select_related('posted_by').prefetch_related('tags').prefetch_related('loved_by').prefetch_related('bookmarked_by').order_by('-created_at').all()
    latest_quotes = Quote.objects.filter(is_approved=True).select_related('posted_by').prefetch_related('tags').prefetch_related('loved_by').prefetch_related('bookmarked_by').order_by('-created_at').all()
    latest_prayers = Prayer.objects.filter(is_approved=True).select_related('posted_by').prefetch_related('tags').prefetch_related('loved_by').prefetch_related('bookmarked_by').order_by('-created_at').all()

    content = list(chain(latest_posts, latest_quotes, latest_prayers))

     # Sort by number of loves first, then by created_at date
    content_sorted = sorted(content, key=lambda x: (-x.loves, -x.created_at.timestamp()))

    return content_sorted

def bookmark_query_for_user(user):
    bookmarked_posts = Post.objects.filter(bookmarked_by=user).select_related('posted_by').prefetch_related('tags').prefetch_related('loved_by').prefetch_related('bookmarked_by').all()
    bookmarked_quotes = Quote.objects.filter(bookmarked_by=user).select_related('posted_by').prefetch_related('tags').prefetch_related('loved_by').prefetch_related('bookmarked_by').all()
    bookmarked_prayers = Prayer.objects.filter(bookmarked_by=user).select_related('posted_by').prefetch_related('tags').prefetch_related('loved_by').prefetch_related('bookmarked_by').all()
    
    bookmarked_content = list(chain(bookmarked_posts, bookmarked_quotes, bookmarked_prayers))
    
    # Sort by number of loves first, then by created_at date
    content_sorted = sorted(bookmarked_content, key=lambda x: (-x.loves, -x.created_at.timestamp()))
    
    return content_sorted

def extract_text_between(text, start, end):
    pattern = re.compile(f'({start}.*?{end})', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1)
    return None 

def love_content_by(request, type: str, id: int) -> tuple:
    """
    Determines the type of content and loves it if the user has not loved it before. 
    
    Parameters:
    - request: HttpRequest object
    - type: str - the type of content to love (i.e. 'post', 'quote', 'prayer')
    - id: int - the id of the content to love
    """

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


    return context, template


def bookmark_content_by(request, type: str, id: int) -> tuple:
    """
    Determines the type of content and bookmarks it if the user has not bookmarked it before. 
    
    Parameters:
    - request: HttpRequest object
    - type: str - the type of content to bookmark (i.e. 'post', 'quote', 'prayer')
    - id: int - the id of the content to bookmark
    """

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

    return context, template