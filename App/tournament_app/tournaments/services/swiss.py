from tournaments.models import Tournament, Participant, JoinTournament, HostTournament, Match, Round
from users.models import User
from tournaments.services.state import InvalidState
import random, math
from decimal import Decimal
from django.db.models import Sum

#Helpers

#Main

def generate_swiss_pairings(tournament: Tournament):
    '''
    Generate pairings for Swiss Format.
    Returns a list of tuples.

    :param tournament: Tournament with the players for the pairings.
    :type tournament: Tournament
    '''
    all_matches = Match.objects.filter(tournament=tournament)
    participants = list(Participant.objects.filter(tournament=tournament).exclude(name='BYE').order_by('-total_points', '-cfc_rating'))
    print(participants)

    if len(participants) % 2 != 0:
        bye, created = Participant.objects.get_or_create(
            name='BYE',
            tournament=tournament,
        )
        participants.append(bye)
    
    pairs =[]
    if Round.objects.last().round_num == 1:
        halfway_point = len(participants) // 2
        upper_half = participants[:halfway_point]
        lower_half = participants[halfway_point:]
        for i in range(halfway_point):
            if i % 2 == 0:
                pairs.append((upper_half[i], lower_half[i]))
            else:
                pairs.append((lower_half[i], upper_half[i]))

    else:
        while len(participants) >= 2:
            p1 = participants.pop(0)
            opponent=None
            white, black = None, None
            played_before_ids = set()
            for ma in all_matches:
                if ma.player_1.uuid == p1.uuid:
                    played_before_ids.add(ma.player_2.uuid)
                elif ma.player_2.uuid == p1.uuid:
                    played_before_ids.add(ma.player_1.uuid)

            opponent_idx = None
            for i, potential_opponent in enumerate(participants):
                if potential_opponent.uuid not in played_before_ids:
                    opponent_idx = i
                    break
            if opponent_idx is not None:
                opponent = participants.pop(opponent_idx)
                if p1.color_balance < opponent.color_balance:
                    white, black  = p1, opponent
                elif p1.color_balance > opponent.color_balance:
                    white, black = opponent, p1
                else:
                    if random.random() > 0.5:
                        white, black = p1, opponent
                    else: 
                        white, black = opponent, p1
                pairs.append((white, black))
            else:
                print('Error: Something went wrong')
            print((white,black))
            print(len(participants))

    return pairs