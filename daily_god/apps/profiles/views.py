from django.shortcuts import render
from django.contrib.auth import logout, login
from allauth.account.forms import LoginForm, SignupForm
from django.urls import reverse, reverse_lazy
from django_htmx.http import HttpResponseClientRedirect, HttpResponseClientRefresh, retarget
from frontend.views import home
from allauth.account.auth_backends import AuthenticationBackend
# Create your views here.
def request_signup(request):
    if request.htmx and request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.clean()
            user, _ = form.try_save(request)
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            response = home(request)
            return retarget(response, '#full_body')
        else:
            context = {'errors': form.errors}
            return render(request, 'profiles/signup.html', context)

    return render(request, 'profiles/signup.html')

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
