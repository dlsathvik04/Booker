from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(req : HttpRequest):
    return render(req, 'books/home.html')

@login_required
def trending(req : HttpRequest):
    return render(req, 'books/trending.html')

@login_required
def new(req: HttpRequest):
    return render(req, 'books/new.html')

@login_required
def list(req: HttpRequest):
    return render(req, 'books/list.html')

@login_required
def recommendations(req: HttpRequest):
    return render(req, 'books/recommendations.html')

@login_required
def details(req : HttpRequest):
    return render(req, 'books/book_details.html')