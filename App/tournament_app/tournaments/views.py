from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from functools import wraps
from .models import Tournament, JoinTournament, Participant, HostTournament, Match, Round
from .forms import CreateTournament, TournamentSettings, RegisterParticipant
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .services import rounds, participants, state, swiss
from django.db.models import Max
import io
import csv

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
                    rounds = rounds.generate_total_number_of_rounds(tournament=tournament),
                    lead_organizer=user,
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
    others = Participant.objects.filter(tournament=tournament).exclude(name='BYE')
    total = int(len(signed_in) + len(others))
    return render(request, 'tournaments/tournament_admin.html', {'tournament': tournament, 'total': total})

@admin_required
def all_participants_in_tournament(request, *args, **kwargs):
    tournament = request.tournament
    signed_in = JoinTournament.objects.filter(tournament=tournament, role = 'PARTICIPANT')
    for si in signed_in:
        rounds.add_user_as_participant(user=si.user, tournament=tournament)
    participants = Participant.objects.filter(tournament=tournament).exclude(name='BYE').order_by('name')
    return render(request, 'tournaments/all_participants.html', {
        'tournament': tournament, 
        'participants': participants,
        'participants_len': len(participants),
        })

@admin_required
def start_tournament(request, *args, **kwargs):
    tournament = request.tournament
    number_of_rounds = int(tournament.rounds)
    number_of_participants = len(Participant.objects.filter(tournament=tournament).exclude(name='BYE'))
    if number_of_participants % 2 == 0 and Participant.objects.filter(name="BYE").exists():
        Participant.objects.get(name='BYE').delete() 
    hosting, created = HostTournament.objects.get_or_create(tournament=tournament)
    round_num = hosting.current_round
    hosting.total_rounds = number_of_rounds
    hosting.save()
    state.close_registration(tournament=tournament)

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
    hosting = get_object_or_404(HostTournament, tournament=tournament)
    hosting.current_round = round_num
    hosting.save()
    tournament_round, created = Round.objects.get_or_create(tournament=tournament, round_num=hosting.current_round)
    print(created)
    if created or tournament_round.matches.count() == 0:
        match tournament.format:
            case 'SWISS':
                pairs = swiss.generate_swiss_pairings(tournament=tournament)
                for idx, pair in enumerate(pairs, start=1):
                    Match.objects.get_or_create(
                            tournament = tournament, 
                            round_num = round_num,
                            player_1 = pair[0],
                            player_2 = pair[1],
                            round_model = tournament_round,
                            ordering = idx  
                        )
                tournament_round.save()

            case _:
                pairs = rounds.generate_pairings(tournament=tournament)
                for idx, pair in enumerate(pairs, start=1):
                    Match.objects.get_or_create(
                            tournament = tournament, 
                            round_num = round_num,
                            player_1 = pair[0],
                            player_2 = pair[1],
                            round_model = tournament_round,
                            ordering = idx  
                        )
                tournament_round.save()

    if Participant.objects.filter(name='BYE').exists():
        bye_player = Participant.objects.get(name='BYE')
        if Match.objects.filter(round_num=round_num, round_model= tournament_round, player_1=bye_player).exists():
            bye_match = Match.objects.get(player_1=bye_player,round_num=round_num, round_model=tournament_round)
            bye_match.p2_points += 1
            bye_match.p1_result = 'LOSS'
            bye_match.p2_result = 'WIN'
            bye_match.isCompleted = True
            bye_match.save()
        else:
            bye_match = Match.objects.get(player_2=bye_player, round_num=round_num, round_model=tournament_round)
            bye_match.p1_points += 1
            bye_match.p2_result = 'LOSS'
            bye_match.p1_result = 'WIN'
            bye_match.isCompleted = True
            bye_match.save()

    rounds.start_round(tournament=tournament)

    print(f'Round ID: {tournament_round.id}')
    print(f'Match count: {tournament_round.matches.count()}')
    print(f'Matches exist: {tournament_round.matches.exists()}')
    for i in range(1, round_num + 1):
        print(i)
    for ma in Match.objects.filter(tournament=tournament, round_num=round_num):
        if ma.isCompleted: 
            print(f'+{ma.p1_points} points for {ma.player_1.name} -- +{ma.p2_points} points for {ma.player_2.name}. COMPLETED')
        else: 
            print(f'Match between {ma.player_1.name} and {ma.player_2.name}: INCOMPLETED')
    
    context = {
        'tournament': tournament,
        'round': tournament_round,
        'round_num': round_num,
    }
    # In the URL, the link requires the tournament uuid and the round_num
    return render(request, 'tournaments/tournament_round.html', context)


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
    for p in Participant.objects.filter(tournament=tournament).exclude(name='BYE'):
        total_points = rounds.derive_points(tournament=tournament, player=p)
        p.total_points = total_points
        p.save()
        p.refresh_from_db()
        
    participants = Participant.objects.filter(tournament=tournament).exclude(name='BYE').order_by('-total_points')
    for ma in matches:
        print(f'{ma.player_1.name}: {ma.player_1.total_points} points -- {ma.player_2.name}: {ma.player_2.total_points} points.')

    next_round_num = int(hosting.current_round) + 1

    context = {
        'tournament': tournament,
        'matches': matches,
        'round_num': round_num,
        'next_round': next_round_num,
        'participants': participants,
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
    tournament.is_finished = True
    tournament.save()

    all_participants = Participant.objects.filter(tournament=tournament).exclude(name='BYE').order_by('-total_points')
    multiple_winners = False
    winning_score = all_participants.aggregate(Max('total_points'))['total_points__max']
    top_participant = all_participants.filter(total_points=winning_score)
    print(top_participant)
    if len(top_participant) >1:
        multiple_winners = True
    context = {
        'tournament': tournament,
        'participants': all_participants, 
        't_winner': top_participant,
        'multiple_winners': multiple_winners,
    }

    return render(request, 'tournaments/tournament_end.html', context)

def add_participant_manually(request, uuid):
    tournament = get_object_or_404(Tournament, uuid=uuid)
    if request.method == "POST":
        form = RegisterParticipant(request.POST)
        if form.is_valid():
            
            with transaction.atomic():
                new_participant = Participant(
                    name=form.cleaned_data['name'],
                    second_name=form.cleaned_data['second_name'],
                    email=form.cleaned_data['email'],
                    cfc_rating=form.cleaned_data['cfc_rating'],
                    fide_rating=form.cleaned_data['fide_rating'],
                    tournament=tournament,
                )
                new_participant.save()
            return redirect('tournaments:all_participants', tournament.uuid)
    else:
        form = RegisterParticipant()
    return render(request, 'tournaments/manual_participant.html', {
        'form': form,
        'tournament': tournament
        })
    
#Action Views

@login_required
def join_tournament(request, uuid):
    tournament = get_object_or_404(Tournament, uuid=uuid)
    if request.method == 'POST':
        JoinTournament.objects.get_or_create(
            user=request.user,
            tournament=tournament
        )
    return redirect('dashboard')

@admin_required
def match_result(request, uuid, round_num, p1_uuid, *args, **kwargs):
    success = False
    p2_result = 'NONE'
    player_1 = get_object_or_404(Participant, uuid=p1_uuid)
    if request.method == "POST":
        tournament = get_object_or_404(Tournament, uuid=uuid)
        match_model = get_object_or_404(Match, tournament=tournament, round_num=round_num, player_1 = player_1)
        result = request.POST.get('result')
        if result in ['WIN', 'DRAW', 'LOSS',]: 
            print(result)
            p1_result, p2_result = rounds.calculate_match_results(result=result, match_model=match_model)
            success = True
            match_model.p1_result = p1_result
            match_model.p2_result = p2_result
            match_model.isCompleted = True
            match_model.save()
            match_model.refresh_from_db()

            print(f'Match {match_model.ordering}: {match_model.player_1.name} {match_model.p1_result} - {match_model.player_2.name} {match_model.p2_result}') 
            print(f'+{match_model.p1_points} points for {match_model.player_1.name} -- +{match_model.p2_points} points for {match_model.player_2.name}')
            print(match_model.isCompleted)
            
        else:
            print('result not valid')
            result = 'NONE'
            p2_result = result
    return JsonResponse({
        'round_num': round_num,
        'player_1': player_1.name,
        'player_2': match_model.player_2.name,
        'result': result,
        'p2_result': p2_result,
        'success': success,
    })


def upload_csv(request, uuid):
    tournament = get_object_or_404(Tournament, uuid=uuid)
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            print('bad')

        else:
            print('good')
            imports, errors = participants.import_participants_from_csv(tournament=tournament, file=csv_file)
            print(imports)
            print(errors)
        for p in Participant.objects.filter(tournament=tournament):
            print(p.name, p.second_name, p.cfc_rating, p.fide_rating, p.email)


            
    return JsonResponse({
        'success': False,
        'message': 'No file received.'
    })

