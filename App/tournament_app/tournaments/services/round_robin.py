from tournaments.models import Tournament, Participant, JoinTournament, HostTournament, Match, Round
from users.models import User
from tournaments.services.state import InvalidState
import random, math
from decimal import Decimal
from django.db.models import Sum

#Main

def generate_round_robin_pairings(tournament: Tournament, round_model=Round):
    participants = list(Participant.objects.filter(tournament=tournament).exclude(name='BYE').order_by('-cfc_rating'))
    
    if len(participants) % 2 != 0:
        bye, created = Participant.objects.get_or_create(
            name='BYE',
            tournament=tournament,
        )
        participants.append(bye)

    fixed = participants[0]
    rotate_list = participants[1:]

    shift = round_model.round_num - 1
    rotate_list = rotate_list[shift:] + rotate_list[:shift]

    new_list = [fixed] + rotate_list

    mid = len(new_list) // 2
    top = new_list[:mid]
    bottom = new_list[mid:][::-1]

    pairings = list(zip(top, bottom))

    return pairings

    