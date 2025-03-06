from django.shortcuts import render
from .forms import PostForm
from .models import Post
from django.http import HttpResponse
from django_htmx.http import reswap, retarget, trigger_client_event
from comments.forms import SeedCommentForm
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import logging

logger = logging.getLogger('app')

# Create your views here.

def get_post(request, id):
    post = cache.get(f'post_{id}')
    if not post:
        try:
            post = Post.objects.get(id=id)
            cache.set(f'post_{id}', post, timeout=60*60) # Cache for 1 hour
        except Post.DoesNotExist:
            post = None

    if post:
        context = {
            'content': post,
            'type': 'post',
        }
        return render(request, 'components/modal.html', context=context)

    return None

@cache_page(60 * 60 * 3)
def blank_form(request):
    return render(request, 'posts/new_post.html#post-form')

def submit_new_post(request):
    post = None
    form = None
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.save(is_being_bookmarked=False, is_being_loved=False)
        else:
            logger.debug(f'Form Errors: {form.errors}')
            context = {'errors': form.errors, 'form': form}
            return render(request, 'posts/new_post.html#post-form', context)

    context = dict(post=post, form=form)

    response = render(request, 'posts/post_content.html', context)
    response = reswap(response, "afterbegin swap:1s")
    response = retarget(response, "#main_content")
    response = trigger_client_event(response, 'reset-new-content-forms', after='receive')

    return response
