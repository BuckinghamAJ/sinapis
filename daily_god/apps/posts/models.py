from django.db import models
from comments.models import Comment
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    url = models.URLField()
    image_url = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    loves = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    comments = models.ManyToManyField(Comment, related_name='posts', 
                                     blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title