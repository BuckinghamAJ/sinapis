from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from profanity.validators import validate_is_profane

# Create your models here.

class Prayer(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField(validators=[validate_is_profane])
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
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