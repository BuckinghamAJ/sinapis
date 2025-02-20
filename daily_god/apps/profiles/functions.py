from .models import Profile
from django.contrib.auth.models import User
import requests
import os
import logging

log = logging.getLogger('app')

class CloudfareServerException(Exception):
    pass

def get_profile_from(user: User):
    profile = Profile.objects.get(user=user)
    return profile

def get_user_from_username(username: str):
    user = User.objects.get(username=username)
    return user

def verify_turnstile(token: str, ip:str) -> bool:
    cf_secret_key = os.getenv('CLOUDFARE_SECRET', None)

    if cf_secret_key is None:
        raise CloudfareServerException("No Cloudfare Secret Key Found")

    log.debug("Sending to CF")

    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        'secret': cf_secret_key,
        'response': token,
        'remoteip': ip
    }

    log.info(f"{data=}")

    response = requests.post(url, data=data)
    result = response.json()

    log.info(f"response: {result}")

    return result.get('success', False)
