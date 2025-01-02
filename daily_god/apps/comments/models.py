from django.db import models
from django.contrib.auth.models import User
from django_comments.abstracts import CommentAbstractModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from profanity.validators import validate_is_profane


COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)

# Create your models here.
class SeedComment(CommentAbstractModel):

    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH, validators=[validate_is_profane])

    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_comments', 
                                           blank=True)
    
    downvoted_by = models.ManyToManyField(User, related_name='downvoted_comments', 
                                          blank=True)