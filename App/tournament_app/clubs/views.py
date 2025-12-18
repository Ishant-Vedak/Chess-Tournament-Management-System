from django.shortcuts import render
from django.http import HttpResponse
from .models import Club

# Create your views here.

def club(request):
    return HttpResponse("this is a sample club")

def all_clubs(request):
    clubs = Club.objects.all()
    context = {
        "clubs": clubs
    }
    return render(request, "clubs/overview.html", context)