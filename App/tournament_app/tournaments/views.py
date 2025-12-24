from django.shortcuts import render
from django.http import HttpResponse
from .models import Tournament
from django.contrib.auth.decorators import login_required
# Create your views here.

def tournament(request):
    return HttpResponse("This is a sample tournament")

def all_tournaments(request):
    tournaments = Tournament.objects.all()

    context = {
        "tournaments": tournaments
    }
    return render(request, "tournaments/overview.html", context)

@login_required
def my_tournaments(request):
    tournaments = request.user.tournaments.all()
    return render(request, "tournaments/user_tournaments.html", {"tournaments": tournaments})