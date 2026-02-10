from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from functools import wraps
from .models import Tournament, JoinTournament, Participant, HostTournament, Match
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
            organizer = JoinTournament.objects.filter(
                user_id =request.user.id, 
                tournament=tournament, 
                role = 'ORGANIZER'
                ).exists()
            admin = JoinTournament.objects.filter(
                user_id =request.user.id, 
                tournament=tournament, 
                role = 'ADMIN'
                ).exists()
            if not (organizer or admin):
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
    for si in signed_in:
        rounds.add_user_as_participant(user=si.user, tournament=tournament)
    participants = Participant.objects.filter(tournament=tournament).exclude(name='BYE')
    return render(request, 'tournaments/all_participants.html', {
        'tournament': tournament, 
        'participants': participants,
        'participants_len': len(participants),
        })

@admin_required
def start_tournament(request, *args, **kwargs):
    tournament = request.tournament
    number_of_rounds = int(tournament.rounds)
    number_of_participants = len(Participant.objects.filter(tournament=tournament))
    hosting, created = HostTournament.objects.get_or_create(tournament=tournament)
    round_num = hosting.current_round
    hosting.total_rounds = number_of_rounds
    hosting.save()
    return render(request, 'tournaments/tournament_confirmation.html', {
        'tournament': tournament, 
        'number_of_rounds': number_of_rounds, 
        'number_of_participants': number_of_participants,
        'round_num': round_num
        })

@admin_required
def hosting_tournament_round(request, uuid, round_num, *args, **kwargs):
    '''
    View for a tournament round. First it should receive the tournament model from request, and give 404 if the uuid doesn't match. Then it should find the related HostTournament model, and if not found then create it. The model should have the total_rounds = tournament.rounds, and the current_round=round_num. Then it should generate the pairings, and then start the round. Starting the round will return a list of tuples, each tuple being a pair in the round. 
    
    :param request: Description
    :param uuid: Tournament UUID
    :param round_num: Description
    :param args: Description
    :param kwargs: Description
    '''
    tournament = get_object_or_404(Tournament, uuid=uuid)
    hosting= get_object_or_404(HostTournament, tournament=tournament)
    hosting.current_round = round_num
    hosting.save()
    matches = []
    m = Match.objects.filter(tournament=tournament, round_num=round_num)
    if m.exists():
        for ma in m:
            matches.append(ma)
    else:
        pairs = rounds.generate_pairings(tournament=tournament)
        for pair in pairs:
            match, created = Match.objects.get_or_create(
                tournament = tournament, 
                round_num = round_num,
                player_1 = pair[0],
                player_2 = pair[1],
            )
            matches.append(match)
    rounds.start_round(tournament=tournament)
    # In the URL, the link requires the tournament uuid and the round_num
    return render(request, 'tournaments/tournament_round.html', {
        'tournament': tournament,
        'matches': matches,
        'round_num': round_num,
    })


@admin_required
def match_result(request, uuid, round_num, p1_uuid, *args, **kwargs):
    success = False
    if request.method == "POST":
        tournament = get_object_or_404(Tournament, uuid=uuid)
        result = request.POST.get('result')
        if result in ['WIN', 'DRAW', 'LOSS']:    
            p2_result = rounds.calculate_match_results(t=tournament, rn=round_num, result=result, p1_uuid=p1_uuid)
            success = True
    else:
        result = 'NONE'
        p2_result = result
    return JsonResponse({
        'result': result,
        'p2_result': p2_result,
        'success': success,
    })


@admin_required
def end_tournament_round(request, uuid, round_num, *args, **kwargs):
    '''
    This view is for ending a round in a live tournament. It should add 1 to the current_round att of the HostTournament model, make the round_is_active att false, and display info about the round, which is what the points of the participants after the round is. 
    
    :param request: Description
    :param uuid: Description
    :param round_num: Description
    :param args: Description
    :param kwargs: Description
    '''
    tournament = get_object_or_404(Tournament, uuid=uuid)
    hosting = get_object_or_404(HostTournament, tournament=tournament)
    matches = Match.objects.filter(tournament=tournament, round_num = round_num)

    rounds.end_round(tournament=tournament)

    next_round_num = int(hosting.current_round) + 1

    context = {
        'tournament': tournament,
        'matches': matches,
        'round_num': round_num,
        'next_round': next_round_num,
    }
    return render(request, 'tournaments/round_end.html', context)

@admin_required
def tournament_settings(request, uuid, *args, **kwargs):
    tournament = kwargs.get('tournament') or get_object_or_404(Tournament, uuid=uuid)
    if request.method == 'POST':
        form = TournamentSettings(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect('tournaments:tournament_admin', tournament.uuid)
    else: 
        form = TournamentSettings(instance=tournament)

    return render(request, 'tournaments/tournament_settings.html', {'tournament': tournament, 'form': form})

@admin_required
def tournament_end(request, uuid, *args, **kwargs):

    tournament = get_object_or_404(Tournament, uuid=uuid)

    context = {
        'tournament': tournament
    }

    return render(request, 'tournaments/tournament_end.html', context)