from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from functools import wraps
from .models import Tournament, JoinTournament, TournamentPermission
from .forms import CreateTournament
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Create your views here.

#Decorators 
def admin_required(view_func=None, *, tournament_uuid='uuid'):
    """Decorator that enforces a user has permission for a tournament.

    Usable as either `@admin_required` or `@admin_required(id_kwarg='uuid')`.
    """
    def _decorator(fn):
        @wraps(fn)
        def wrapped_func(request, *args, **kwargs):
            # Accept uuid passed either as a kwarg or as the first positional arg
            uuid = kwargs.get(tournament_uuid)
            if uuid is None and args:
                uuid = args[0]
            tournament = get_object_or_404(Tournament, uuid=uuid)
            request.tournament = tournament
            if not TournamentPermission.objects.filter(user=request.user, tournament=tournament).exists():
                return HttpResponseForbidden("You do not have permission to view this page.")
            # Pass tournament to the wrapped view via kwargs so view signatures stay flexible
            kwargs['tournament'] = tournament
            return fn(request, *args, **kwargs)
        return wrapped_func 

    if view_func is None:
        return _decorator
    return _decorator(view_func)



#Functions
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
                permissions = TournamentPermission(
                    user=user,
                    tournament=tournament
                )
                permissions.save()
            return redirect('tournaments:confirm_tournament')
    else:
        form = CreateTournament()
    return render(request, 'tournaments/create_tournament.html', {'form': form})

@login_required
def my_tournaments(request):
    user = request.user
    admin_tournaments = []
    joined_tournaments = []
    user_tournaments = user.tournaments.all()
    for t in user_tournaments:
        if TournamentPermission.objects.filter(user=user, tournament=t).exists():
            admin_tournaments.append(t)
        joined_tournaments.append(t)
        continue
    return render(request, 'tournaments/user_tournaments.html', {'tournaments': joined_tournaments, 'admin_tournaments': admin_tournaments})

def confirm_tournament(request):
    tournament = request.user.tournaments.latest()
    return render(request, 'tournaments/otp_page.html', {'tournament': tournament})

@admin_required
def tournament_admin(request, *args, **kwargs):
    tournament = request.tournament
    return render(request, 'tournaments/tournament_admin.html', {'tournament': tournament})