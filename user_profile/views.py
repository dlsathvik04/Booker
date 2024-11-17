from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here

@login_required
def profile_view(req : HttpRequest):
    return render(req, 'profile/profile.html')


@login_required
def profile_edit(req : HttpRequest):
    if req.method == 'GET':
        print(req.user.pk)