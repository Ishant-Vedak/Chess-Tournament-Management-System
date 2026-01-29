from tournaments.models import Tournament, Participant, JoinTournament, TournamentPermission
from users.models import User
from tournaments.services.state import InvalidState
import random

def add_user_as_participant(user: User, tournament: Tournament):
    '''
    Takes info from the JoinTournament Model and creates a Participant Model for it.
    
    :param user: User in the JoinTournament Model.
    :type user: User
    :param tournament: Tournament in the JoinTournament Model.
    :type tournament: Tournament
    '''

    participant, create = Participant.objects.get_or_create(
        name=user.username,
        user=user,
        tournament=tournament,
        random_seed=random.randint(1, 1_000_000)

    )
    return participant

def generate_pairings(tournament: Tournament):
    '''
    Generates pairings for a round. 
    
    :param tournament: Tournament with the players for the pairings.
    :type tournament: Tournament
    '''
    joins = JoinTournament.objects.filter(tournament=tournament)
    participants = Participant.objects.filter(tournament=tournament)
    for j in joins:
            add_user_as_participant(user=j.user, tournament=j.tournament)
    for p in participants:
        p.random_seed = random.randint(1, 1_000_000)
        p.save()
    
    participants_sorted = sorted(participants, key=lambda p:p.random_seed)

    pairs = [(participants_sorted[i], participants_sorted[i + 1]) for i in range(0, len(participants), 2)]
    return pairs
    



    