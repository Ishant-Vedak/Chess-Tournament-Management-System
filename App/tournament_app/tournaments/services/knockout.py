from tournaments.models import Tournament, Participant, JoinTournament, HostTournament, Match, Round
from users.models import User
from tournaments.services.state import InvalidState
import random, math
from decimal import Decimal
from django.db.models import Sum, Q


def generate_knockout_pairings(tournament: Tournament, round_model: Round):
    participants = list(Participant.objects.filter(tournament=tournament).exclude(name='BYE').order_by('-cfc_rating'))
    latest_round_num = round_model.round_num

    if latest_round_num > 1:

        p1_losers = Match.objects.filter(tournament=tournament,p1_result='LOSS').values_list('player_1_id', flat=True)
        p2_losers = Match.objects.filter(tournament=tournament,p2_result='LOSS').values_list('player_2_id', flat=True)
        all_losers = set(list(p1_losers) + list(p2_losers))
        participants = [p for p in participants if p.id not in all_losers]

    n = len(participants)
    print(f'Total Participants: {n}')

    next_power_of_2 = 2 ** math.ceil(math.log2(n))
    number_of_byes = next_power_of_2 - n
    print(f'Number of Byes: {number_of_byes}')

    if number_of_byes == 0:
        mid = n // 2
        return list(zip(participants[:mid], participants[mid:][::-1]))
    
    num_playing_players = n - number_of_byes #Can be used to check if code works properly later.

    bye_player, created = Participant.objects.get_or_create(
                name='BYE',
                tournament=tournament,
            )
    for idx, player in enumerate(participants[:number_of_byes]):  
        new_match, created = Match.objects.get_or_create(
            player_1 = player,
            player_2 = bye_player,
            tournament=tournament,
            round_num = latest_round_num,
            round_model = round_model,
        )
        print(idx)
    playing_players = participants[number_of_byes:]
    mid = len(playing_players) // 2
    return list(zip(playing_players[:mid], playing_players[mid:][::-1]))

