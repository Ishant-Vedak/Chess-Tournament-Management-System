from tournaments.models import Tournament, Participant
from tournaments.services.state import InvalidState

def add_participant(
        t: Tournament, 
        name: str, 
        email: str | None = None, 
        rating: str | None = None,
        user=None
        ):
    
    '''
    Docstring for add_participant

    Checks if tournament registration is open. If it is, allows participants to be added. Otherwise, error.
    
    :param t: Tournament which the participant will be added to.
    :type t: Tournament
    :param name: Name of participant imported, either through csv or json.
    :type name: str
    :param email: Email of participant, but optional.
    :type email: str | None
    :param rating: Rating of participant, but optional.
    :type rating: str | None
    :param user: If the participant is logged in, they can use their account. Currently not addressing this. 
    '''
    tournament = t
    if tournament.status != "REGISTRATION_OPEN":
        raise InvalidState("Registration is not open, Participants cannot be added.")
    Participant.objects.create(name=name, tournament=tournament, email=email, rating=rating)