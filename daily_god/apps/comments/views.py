from django.shortcuts import render

# Django Comments
from comments.forms import SeedCommentForm
from django import http
from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django_comments.views.comments import CommentPostBadRequest
from .models import SeedComment


import django_comments
from django_comments import signals
from logging import getLogger


log = getLogger('app')

# Create your views here.
@csrf_protect
@require_POST
def post_comment(request, next=None, using=None):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    log.debug(data)
    if request.user.is_authenticated:
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.get_username()
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")

    log.debug(f'ctype: {ctype}')
    log.debug(f'object_pk: {object_pk}')
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = apps.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except (LookupError, TypeError) as e:
        log.error(e)
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % (
                escape(ctype), escape(object_pk)))
    except (ValueError, ValidationError) as e:
        return CommentPostBadRequest(
            "Attempting to get content-type %r and object PK %r raised %s" % (
                escape(ctype), escape(object_pk), e.__class__.__name__))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = django_comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % escape(str(form.security_errors())))

    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        template_list = [
            # These first two exist for purely historical reasons.
            # Django v1.0 and v1.1 allowed the underscore format for
            # preview templates, so we have to preserve that format.
            "comments/%s_%s_preview.html" % (model._meta.app_label, model._meta.model_name),
            "comments/%s_preview.html" % model._meta.app_label,
            # Now the usual directory based template hierarchy.
            "comments/%s/%s/preview.html" % (model._meta.app_label, model._meta.model_name),
            "comments/%s/preview.html" % model._meta.app_label,
            "comments/preview.html",
        ]
        return render(request, template_list, {
                "comment": form.data.get("comment", ""),
                "form": form,
                "next": data.get("next", next),
            },
        )

    # Otherwise create the comment
    comment = form.get_comment_object(site_id=get_current_site(request).id)
    comment.ip_address = request.META.get("REMOTE_ADDR", None) or None
    if request.user.is_authenticated:
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    for (receiver, response) in responses:
        if response is False:
            return CommentPostBadRequest(
                "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    return render(request, 'comments/comments.html#comment-list', {'content': target, })

def get_comment(id):
    comment = SeedComment.objects.filter(id=id).prefetch_related('upvoted_by', 'downvoted_by').first()
    return comment

def upvote(request, id):
    comment = get_comment(id)

    if comment and request.user not in comment.upvoted_by.all():
        comment.upvoted_by.add(request.user)

        if request.user in comment.downvoted_by.all():
            comment.downvoted_by.remove(request.user)
            comment.downvotes -= 1

        comment.upvotes += 1
    else:
        comment.upvoted_by.remove(request.user)
        comment.upvotes -= 1

    comment.save()

    return render(request, 'comments/comments.html#upvote-downvote', {'comment': comment })

def downvote(request, id):
    comment = get_comment(id)

    if comment and request.user not in comment.downvoted_by.all():
        comment.downvoted_by.add(request.user)

        if request.user in comment.upvoted_by.all():
            comment.upvoted_by.remove(request.user)
            comment.upvotes -= 1

        comment.downvotes += 1
    else:
        comment.downvoted_by.remove(request.user)
        comment.downvotes -= 1

    comment.save()

    return render(request, 'comments/comments.html#upvote-downvote', {'comment': comment, })