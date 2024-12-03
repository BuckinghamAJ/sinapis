from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from pathlib import Path

profile_pic_default = Path('static', 'img', 'default_pfp.jpg')

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', default=str(profile_pic_default))
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'