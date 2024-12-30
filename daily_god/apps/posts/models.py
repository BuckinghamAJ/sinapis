from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf import settings
from profanity.validators import validate_is_profane

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

    def save(self, *args, **kwargs):
        if self.posted_by.profile.trust_level >= settings.TRUST_LEVEL_THRESHOLD and\
            not self.posted_by.profile.is_banned and\
            not self.posted_by.profile.under_review:  # Adjust the trust level threshold as needed
            
            self.is_approved = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['is_approved']),
        ]