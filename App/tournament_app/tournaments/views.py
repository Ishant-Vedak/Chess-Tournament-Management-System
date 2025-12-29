from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Tournament, JoinTournament
from .forms import CreateTournament
from django.contrib.auth.decorators import login_required
from django.db import transaction
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
    if request.method == "POST":
        form = CreateTournament(request.POST)
        if form.is_valid():
            user = request.user
            with transaction.atomic():
                tournament = Tournament(
                    name=form.cleaned_data['name'],
                    status=form.cleaned_data['status'],
                    type=form.cleaned_data['type'], 
                    club = form.cleaned_data['club'],
                    lead_organizer=user
                )
                tournament.save()
                join = JoinTournament(
                    user=user,
                    tournament=tournament,
                    role="ORGANIZER",
                )
                join.save()
            return redirect('dashboard')
    else:
        form = CreateTournament()
    return render(request, 'tournaments/create_tournament.html', {'form': form})

@login_required
def my_tournaments(request):
    tournaments = request.user.tournaments.all()
    return render(request, "tournaments/user_tournaments.html", {"tournaments": tournaments})