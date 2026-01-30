from tournaments.models import Tournament, Participant, JoinTournament, HostTournament
from users.models import User
from tournaments.services.state import InvalidState
import random, math

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
    

# Use if organizers did not put number of rounds.
def generate_total_number_of_rounds(tournament: Tournament):
    '''
    Generates the total number of rounds for a tournament based on the format.
    
    :param tournament: The tournament for which rounds need to be decided.
    :type tournament: Tournament
    '''
    joins = JoinTournament.objects.filter(tournament=tournament, role='PARTICIPANT')
    participants = Participant.objects.filter(tournament=tournament)

    total_participants = int(joins) + int(participants)
    num_of_rounds = 0

    if tournament.format == 'SWISS':
        if 8 <= total_participants <= 16:
             num_of_rounds = 5
        elif 17 <= total_participants <= 32:
             num_of_rounds = 6
        elif 33 <= total_participants <= 64:
             num_of_rounds = 7
        else:
             num_of_rounds = 0

    if tournament.format == 'ROUND_ROBIN':
        num_of_rounds = int(total_participants - 1)
    
    if tournament.format == 'KNOCKOUT':
        num_of_rounds = math.ceil(math.log2(total_participants))

    return num_of_rounds


    