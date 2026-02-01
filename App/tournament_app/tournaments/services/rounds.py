from tournaments.models import Tournament, Participant, JoinTournament, HostTournament
from users.models import User
from tournaments.services.state import InvalidState
import random, math

def add_user_as_participant(user: User, tournament: Tournament):
    '''
    Takes info from the JoinTournament Model and creates a Participant Model for it.
    Returns a Participant model.
    
    :param user: User in the JoinTournament Model.
    :type user: User
    :param tournament: Tournament in the JoinTournament Model.
    :type tournament: Tournament
    '''

    participant, create = Participant.objects.get_or_create(
        user=user,
        tournament=tournament,
        defaults={
           "random_seed": random.randint(1, 1_000_000),
           "name": user.username,
        }
        

    )
    return participant

def generate_pairings(tournament: Tournament):
    '''
    Generates pairings for a round. 
    Returns a list of tuples.
    
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
    
    if len(participants) % 2 != 0:
        bye = Participant.objects.create(
            tournament = tournament, 
            name = 'BYE',
            random_seed = random.randint(1, 1_000_000)
        )
        bye.save()

    participants = Participant.objects.filter(tournament=tournament)
    participants_sorted = sorted(participants, key=lambda p:p.random_seed)

    pairs = [[participants_sorted[i], participants_sorted[i + 1]] for i in range(0, len(participants_sorted) - 1, 2)]
    return pairs
    

# Use if organizers did not put number of rounds.
def generate_total_number_of_rounds(tournament: Tournament):
    '''
    Generates the total number of rounds for a tournament based on the format.
    Returns an integer.
    
    :param tournament: The tournament for which rounds need to be decided.
    :type tournament: Tournament
    '''
    joins = JoinTournament.objects.filter(tournament=tournament, role='PARTICIPANT').count()

    participants = Participant.objects.filter(tournament=tournament).count()

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

    elif tournament.format == 'ROUND_ROBIN':
        num_of_rounds = int(total_participants - 1)
    
    elif tournament.format == 'KNOCKOUT':
        num_of_rounds = math.ceil(math.log2(total_participants))

    else:
         raise InvalidState("Tournament does not have correct format.")

    # Double Elim is for later.

    return num_of_rounds


def start_round(tournament: Tournament):
    '''
    Starts a round for a tournament.
    Returns nothing.
    
    :param tournament: The tournament for which a round is starting.
    :type tournament: Tournament
    '''
    hosting = HostTournament.objects.get(tournament=tournament)

    if hosting.total_rounds == 0:
         raise InvalidState("Tournament does not have any rounds.")
    
    hosting.round_is_active = True
    hosting.save()



def end_round(tournament: Tournament):
    '''
    End a round in a tournament.
    Returns nothing.
    
    :param tournament: The tournament for which a round is ending.
    :type tournament: Tournament
    '''

    hosting = HostTournament.objects.get(tournament=tournament)

    if hosting.total_rounds == 0:
         raise InvalidState("Tournament does not have any rounds.")
    
    hosting.round_is_active = False
    hosting.save()

def step_round(tournament: Tournament):
    '''
    Increases the current round by 1. 
    Returns an integer for the current round of the HostTournament model.
    
    :param tournament: The tournament for which the round_number is increasing.
    :type tournament: Tournament
    '''
    hosting = HostTournament.objects.get(tournament=tournament)

    if hosting.round_is_active:
        return int(hosting.current_round)
    hosting.current_round += 1
    hosting.round_is_active = True
    hosting.save()

    return int(hosting.current_round)

    