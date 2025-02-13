from .models import Profile
from django.contrib.auth.models import User

def get_profile_from(user: User):
    profile = Profile.objects.get(user=user)
    return profile

def get_user_from_username(username: str):
    user = User.objects.get(username=username)
    return user