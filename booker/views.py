
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def landing_view(req : HttpRequest):
    return render(req, 'booker/landing.html')

def login_view(req : HttpRequest):
    if (req.method == 'POST'):
        print(req.POST)
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('/home/')
        else:
            return render(req, 'booker/login.html', {'login_failed' : True})

    return render(req, 'booker/login.html')

def logout_view(req : HttpRequest):
    logout(req)
    return render(req, 'booker/login.html')


def register_view(req : HttpRequest):
    if (req.method == 'POST'):
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name = last_name)
        user.save()
        return render(req, 'booker/register.html')
    return render(req, 'booker/register.html')