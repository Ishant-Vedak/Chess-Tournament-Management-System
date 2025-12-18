from django.shortcuts import render
from django.http import HttpResponse
from .models import User

# Create your views here.

def user(request):
    return HttpResponse("This is a sample user")

def all_users(request):
    users = User.objects.all()

    context = {
        "users": users
    }

    return render(request, "users/overview.html", context)