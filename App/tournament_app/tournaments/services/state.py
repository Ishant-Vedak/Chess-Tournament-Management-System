from django.core.exceptions import PermissionDenied
from tournaments.models import Tournament

class InvalidState(Exception):
    pass

#Changing states
def open_registration(tournament: Tournament):
    '''
    Opens registration if its in draft, otherwise raises an error.
    '''
    if tournament.status != "DRAFT":
        raise InvalidState("Registration is open.")
    tournament.status = "REGISTRATION_OPEN"
    tournament.save()
    return tournament

def close_registration(tournament: Tournament):
    '''
    Closes registration if its open, otherwise raises an error.
    '''
    if tournament.status != "REGISTRATION_OPEN":
        raise InvalidState("Registration is closed.")
    tournament.status = "REGISTRATION_CLOSED"
    tournament.save()
    return tournament

def start_tournament(tournament: Tournament):
    '''
    Starts tournament when registration is closed, otherwise raises an error.
    '''
    if tournament.status != "REGISTRATION_CLOSED":
        raise InvalidState("Registration is still open.")
    tournament.status = "ONGOING"
    tournament.save()
    return tournament

def end_tournament(tournament: Tournament):
    '''
    Ends tournament when its ongoing, otherwise raises an error.
    '''
    if tournament.status != "ONGOING":
        raise InvalidState("Tournament is ongoing.")
    tournament.status = "CLOSED"
    tournament.save()
    return tournament