from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf import settings
from frontend.validators import validate_is_profane
from embed_video.fields import EmbedVideoField

import logging
log = logging.getLogger('app')

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, validators=[validate_is_profane])
    summary = models.TextField(max_length=3000, blank=False, null=False, validators=[validate_is_profane])
    url = models.URLField()
    image_url = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    loves = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)

    video = EmbedVideoField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    reports = models.PositiveIntegerField(default=0)

    loved_by = models.ManyToManyField(User, related_name='loved_posts',
                                      blank=True)
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_posts',
                                           blank=True)

    _is_twitter = None

    @property
    def is_twitter(self) -> bool:
        if self._is_twitter is None:
            self._is_twitter = False
            if ('twitter' in str(self.url)):
                self._is_twitter = True
        return self._is_twitter


    def save(self, *args, is_being_bookmarked: bool = False, is_being_loved: bool = False, **kwargs):

        is_bookmarked: bool = is_being_bookmarked
        is_loved: bool = is_being_loved

        if not is_bookmarked and not is_loved:
            if self.url_to_embeded_video(self.url):
                self.video = self.url

            if self.trust_user():
                self.is_pending = False
                self.is_approved = True

        super().save(*args, **kwargs)

    def trust_user(self):
        if self.posted_by.profile.trust_level >= settings.TRUST_LEVEL_THRESHOLD and\
            not self.posted_by.profile.is_banned and\
            not self.posted_by.profile.under_review:
                return True
        return False

    @staticmethod
    def url_to_embeded_video(url):
        url = url.lower()
        if (('youtube' in url) or
            ('youtu.be' in url) or
            ('vimeo' in url)):
            return True
        return False

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['is_approved']),
        ]
