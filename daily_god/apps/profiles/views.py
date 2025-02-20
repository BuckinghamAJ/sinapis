from django.shortcuts import render
from django.contrib.auth import logout, login
from allauth.account.forms import LoginForm, SignupForm
from django.urls import reverse, reverse_lazy
from django_htmx.http import HttpResponseClientRedirect, HttpResponseClientRefresh, retarget, trigger_client_event
from frontend.views import home
from allauth.account.auth_backends import AuthenticationBackend
from .functions import get_user_from_username, verify_turnstile, CloudfareServerException
from django.template import Template, Context
from django.http import HttpResponse
from .forms import ProfileForm, UserForm

import logging
import os 
log = logging.getLogger('app')

CLOUDFARE_SITEKEY= os.getenv('CLOUDFARE_SITEKEY', "0x4AAAAAAA9VV9NxwQS-MzX9")

# Create your views here.
def request_signup(request):
    
    if request.htmx and request.method == 'POST':
        log.debug(f"{request.POST=}")

        form = SignupForm(request.POST)
        token = request.POST.get("cf-turnstile-response")
        remoteip = request.META.get('REMOTE_ADDR')

        try:
            if form.is_valid() and verify_turnstile(token, remoteip):
                form.clean()
                user, _ = form.try_save(request)
                login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                response = home(request)
                return retarget(response, '#base-content')
            else:
                context = {'errors': form.errors, 'cf_sitekey': CLOUDFARE_SITEKEY}
                return render(request, 'profiles/signup.html', context)

        except CloudfareServerException as e:
            context = {'errors': {"cf": str(e) }, 'cf_sitekey': CLOUDFARE_SITEKEY}
            return render(request, 'profiles/signup.html', context)

    return render(request, 'profiles/signup.html', {'cf_sitekey': CLOUDFARE_SITEKEY})

def request_login(request):
    if request.htmx and request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            form.clean()
            form.login(request, redirect_url=reverse_lazy('home'))
            response = home(request)
            return retarget(response, '#base-content')
        else:
            context = {'errors': form.errors}
            return render(request, 'profiles/login.html', context)

    return render(request, 'profiles/login.html')

def request_account_reset(request):
    return render(request, 'profiles/account_reset.html')

def profile_logout(request):
    logout(request)

    return home(request)

def get_profile(request):
    return render(request, 'profiles/profile.html')

def get_profile_pic(request):
    img_temp = Template("""<img id="topbar_profile_pic"
                alt="Profile picture of user"
                src="{{ user.profile.profile_pic.url }}" />""")
    
    img_context = Context({'user': request.user})

    return HttpResponse(img_temp.render(img_context))


def update_profile(request):
    profile_form = ProfileForm()

    if request.htmx and request.method == 'POST':

        username = request.user.username
        user = get_user_from_username(username)
        log.debug(f"Files sent: {request.FILES}")
        
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        user_form = UserForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            
            response = render(request, 'profiles/profile.html')

            if request.FILES:
               response = trigger_client_event(
                                response,
                                'profile-pic-updated'
                        )

            return response
        else:
            errors = profile_form.errors.copy()
            errors.update(user_form.errors)
            context = {'errors': errors}
            return render(request, 'profiles/profile.html', context)

    return render(request, 'profiles/profile.html#profile-form', context={'profile_form': profile_form})    