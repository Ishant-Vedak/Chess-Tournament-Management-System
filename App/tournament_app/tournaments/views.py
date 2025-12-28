from django.shortcuts import render, get_object_or_404
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

def tournament_details(request, uuid):
    tournament = get_object_or_404(Tournament, uuid=uuid)
    return render(request, 'tournaments/detail.html', {"tournament": tournament})

@login_required
def create_tournament(request):
    ...

@login_required
def my_tournaments(request):
    tournaments = request.user.tournaments.all()
    return render(request, "tournaments/user_tournaments.html", {"tournaments": tournaments})


@login_required
def join_tournament(request):
    ...