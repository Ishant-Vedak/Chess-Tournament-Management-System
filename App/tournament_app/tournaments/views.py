from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from functools import wraps
from .models import Tournament, JoinTournament, Participant, HostTournament
from .forms import CreateTournament, TournamentSettings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .services import rounds
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
            if not JoinTournament.objects.filter(user=request.user, tournament=tournament, role__in= ['ADMIN', 'ORGANIZER']).exists():
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
def join_tournament(request, uuid):
    tournament = get_object_or_404(Tournament, uuid=uuid)
    if request.method == 'POST':
        JoinTournament.objects.get_or_create(
            user=request.user,
            tournament=tournament
        )
    return redirect('dashboard')

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
                    club=form.cleaned_data['club'],
                    rounds=form.cleaned_data['rounds'],
                    lead_organizer=user
                )
                tournament.save()
                join = JoinTournament(
                    user=user,
                    tournament=tournament,
                    role="ORGANIZER",
                )
                join.save()
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
        if JoinTournament.objects.filter(user=user, tournament=t).exists():
            admin_tournaments.append(t)
            continue
        joined_tournaments.append(t)
        continue
    return render(request, 'tournaments/user_tournaments.html', {'tournaments': joined_tournaments, 'admin_tournaments': admin_tournaments})

def confirm_tournament(request):
    tournament = request.user.tournaments.latest()
    return render(request, 'tournaments/otp_page.html', {'tournament': tournament})

# Tournament Admin - Before Hosting

@admin_required
def main_tournament_page(request, *args, **kwargs):
    ...

@admin_required
def tournament_admin(request, *args, **kwargs):
    tournament = request.tournament
    signed_in = JoinTournament.objects.filter(tournament=tournament, role = 'PARTICIPANT')
    others = Participant.objects.filter(tournament=tournament)
    total = int(len(signed_in) + len(others))
    return render(request, 'tournaments/tournament_admin.html', {'tournament': tournament, 'total': total})

@admin_required
def all_participants_in_tournament(request, *args, **kwargs):
    tournament = request.tournament
    signed_in = JoinTournament.objects.filter(tournament=tournament, role = 'PARTICIPANT')
    others = Participant.objects.filter(tournament=tournament)
    return render(request, 'tournaments/all_participants.html', {'participants': signed_in, 'tournament': tournament, 'others': others})

@admin_required
def start_tournament(request, *args, **kwargs):
    tournament = request.tournament
    number_of_rounds = int(tournament.rounds)
    number_of_participants = len(Participant.objects.filter(tournament=tournament))
    return render(request, 'tournaments/tournament_confirmation.html', {'tournament': tournament, 'number_of_rounds': number_of_rounds, 'number_of_participants': number_of_participants})

@admin_required
def hosting_tournament_round(request, uuid):
    tournament = get_object_or_404(Tournament, uuid=uuid)
    hosting = HostTournament.objects.create(tournament=tournament)
    hosting.total_rounds = tournament.rounds
    rounds.generate_pairings(tournament=tournament)


@admin_required
def tournament_settings(request, uuid, **kwargs):
    tournament = kwargs.get('tournament') or get_object_or_404(Tournament, uuid=uuid)
    if request.method == 'POST':
        form = TournamentSettings(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect('tournaments:tournament_admin', tournament.uuid)
    else: 
        form = TournamentSettings(instance=tournament)

    return render(request, 'tournaments/tournament_settings.html', {'tournament': tournament, 'form': form})

# Tournament Admin - After Hosting