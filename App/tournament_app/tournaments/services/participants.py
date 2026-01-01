from tournaments.models import Tournament, Participant
from tournaments.services.state import InvalidState
import csv

def add_participant(
        tournament: Tournament, 
        name: str, 
        email: str | None = None, 
        rating: int | None = None,
        user=None
        ):
    
    '''
    Docstring for add_participant

    Checks if tournament registration is open. If it is, allows participants to be added. Otherwise, error.
    
    :param tournament: Tournament which the participant will be added to.
    :type tournament: Tournament
    :param name: Name of participant imported, either through csv or json.
    :type name: str
    :param email: Email of participant, but optional.
    :type email: str | None
    :param rating: Rating of participant, but optional.
    :type rating: str | None
    :param user: If the participant is logged in, they can use their account. Currently not addressing this. 
    '''
    t = tournament
    if t.status != "REGISTRATION_OPEN":
        raise InvalidState("Registration is not open, Participants cannot be added.")
    Participant.objects.create(name=name, tournament=t, email=email, rating=rating)

def import_participants_from_csv(tournament: Tournament, file):
    '''
    Docstring for import_participants_from_csv

    Imports all participants from a csv file provided by organizers. 
    
    :param tournament: Tournament for the participants. 
    :type tournament: Tournament
    :param file: CSV file containing names of participants. Must have a name column, and could have an email and rating column.
    :type file: file-like object
    '''
    errors = []
    import_count = 0
    
    reader = csv.DictReader(file)

    if not "name" in reader.fieldnames:
        raise ValueError("CSV File is missing column 'name' ")

    for i, row in enumerate(reader, start=1):
        name = row.get('name', '').strip()
        email = row.get('email', '').strip() or None
        rating = row.get('rating', '').strip() or None

        if not name: 
            errors.append(f'Row {i}: Missing name')
            continue

        if rating is not None:
            try: 
                rating = int(rating)
            except ValueError:
                errors.append(f'Row {i}: Invalid Rating "{row.get('rating')}".')
                continue
        try: 
            add_participant(tournament=tournament, name=name, email=email, rating=rating)
            import_count += 1 
        except InvalidState as e:
            errors.append(f'Row {i}: {str(e)}')
            
    return import_count, errors