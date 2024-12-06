from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from posts.models import Post
from comments.models import Comment

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Post)
def update_trust_level_on_post(sender, instance, created, **kwargs):
    if created:
        profile = instance.posted_by.profile
        profile.trust_level += 1  # Increase trust level for creating a post
        profile.save()

@receiver(post_save, sender=Comment)
def update_trust_level_on_comment(sender, instance, created, **kwargs):
    if created:
        profile = instance.author.profile
        profile.trust_level += 1  # Increase trust level for creating a comment
        profile.save()

@receiver(post_save, sender=Post)
def update_trust_level_on_love(sender, instance, **kwargs):
    profile = instance.posted_by.profile
    profile.trust_level += instance.loves  # Increase trust level based on loves received
    profile.save()