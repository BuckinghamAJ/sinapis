from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.
def request_signup(request):
    return render(request, 'profiles/signup.html')

def request_login(request):
    return render(request, 'profiles/login.html')

def request_account_reset(request):
    return render(request, 'profiles/account_reset.html')

def profile_logout(request):
    logout(request)
    return render(request, 'components/topbar.html')