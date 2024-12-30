from posts.models import Post
from posts.forms import PostForm
from quotes.models import Quote
from prayers.models import Prayer
from itertools import chain


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