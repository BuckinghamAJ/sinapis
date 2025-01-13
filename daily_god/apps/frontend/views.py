from django.shortcuts import render
from django.http import HttpResponse

from posts.models import Post
from posts.forms import PostForm
from quotes.models import Quote
from prayers.models import Prayer
from itertools import chain

from .functions import love_content_by, bookmark_content_by, home_query, bookmark_query_for_user

import django_comments
from django_comments import signals
from logging import getLogger
from django.core.paginator import Paginator


log = getLogger('app')


# Create your views here.

def home(request):
    page_number = request.GET.get('page', 1)
    content = home_query()

    # TODO: Infinite Pagination with Scroll: https://aisaastemplate.com/blog/guide-django-pagination/
    paginator = Paginator(content, 16) # Show 10 content per page.

    pg_content = paginator.get_page(page_number)


    context = {
        'content': pg_content,
    }

    if request.GET.get('component') == 'sidebar':
        return render(request, 'content.html#content-list', context=context)
        

    return render(request, 'index.html', context)


def bookmarked(request):
    
    content = bookmark_query_for_user(request.user)

    context = {
        'content': content,
        'user': request.user,
    }

    return render(request, 'content.html#content-list', context=context)

def love_content(request, type, id):
    context, template = love_content_by(request, type, id)
    log.debug(context)
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

