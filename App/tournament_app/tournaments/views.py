from django.shortcuts import render
from django.http import HttpResponse
from .models import Tournament
# Create your views here.

def tournament(request):
    return HttpResponse("This is a sample tournament")

def all_tournaments(request):
    tournaments = Tournament.objects.all()

    context = {
        "tournaments": tournaments
    }
    return render(request, "tournaments/overview.html", context)