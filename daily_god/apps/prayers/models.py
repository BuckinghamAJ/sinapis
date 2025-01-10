from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from profanity.validators import validate_is_profane
from django.conf import settings

# Create your models here.

class Prayer(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField(validators=[validate_is_profane])
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    citation = models.CharField(max_length=100, blank=True)
    loves = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    loved_by = models.ManyToManyField(User, related_name='loved_prayers', 
                                      blank=True)
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_prayers', 
                                           blank=True)

    def __str__(self):
        return f'Prayer by {self.author}'
    
    def save(self, *args, **kwargs):
        if self.posted_by.profile.trust_level >= settings.TRUST_LEVEL_THRESHOLD and\
            not self.posted_by.profile.is_banned and\
            not self.posted_by.profile.under_review:  # Adjust the trust level threshold as needed

            self.is_pending = False
            self.is_approved = True
        super().save(*args, **kwargs)