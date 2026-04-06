from tournaments.models import Tournament, Participant
from tournaments.services.state import InvalidState
import csv
import io

def add_participant(
        tournament: Tournament, 
        name: str, 
        second_name: str | None = None,
        email: str | None = None, 
        cfc_rating: int | None = None,
        fide_rating: int | None = None,
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
    :param cfc_rating: CFC Rating of participant, but optional.
    :type rating: str | None
    :param fide_rating: FIDE Rating of participant, but optional.
    :type rating: str | None
    :param user: If the participant is logged in, they can use their account. Currently not addressing this. 
    '''
    t = tournament
    if t.status != "REGISTRATION_OPEN":
        raise InvalidState("Registration is not open, Participants cannot be added.")
    new, created = Participant.objects.get_or_create(
        name=name, 
        second_name=second_name, 
        tournament=t, email=email, 
        cfc_rating=cfc_rating, 
        fide_rating=fide_rating
        )

def new_headers(initial_fieldnames: list):
    given_headers = initial_fieldnames[:]
    first_name_found = False
    for i, header in enumerate(given_headers):
        lowered = str(header).lower()
        if 'name' in lowered:
            if 'middle' in lowered or 'user' in lowered:
                continue
            if not first_name_found:
                given_headers[i] = 'first_name'
                first_name_found =True
            else: 
                given_headers[i] = 'last_name'
        elif 'elo' in lowered or 'fide' in lowered:
            given_headers[i] = 'fide_rating'
        elif 'cfc' in lowered:
            given_headers[i] = 'cfc_rating'
        else:
            given_headers[i] = lowered
    return given_headers


    

def import_participants_from_csv(tournament: Tournament, file):
    '''
    Docstring for import_participants_from_csv

    Imports all participants from a csv file provided by organizers. 
    
    :param tournament: Tournament for the participants. 
    :type tournament: Tournament
    :param file: CSV file containing names of participants. Must have a name column, and could have an email and CFC rating column.
    :type file: file-like object
    '''
    errors = []
    import_count = 0

    data = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(data), skipinitialspace=True)

    reader.fieldnames = new_headers(reader.fieldnames)
    print(reader.fieldnames)

    for idx, row in enumerate(reader, start=1):
        try:
            add_participant(
                tournament=tournament, 
                name=row.get('first_name'),
                second_name=row.get('last_name'),
                email=row.get('email'),
                cfc_rating=row.get('cfc_rating'),
                fide_rating=row.get('fide_rating')
            )
            import_count += 1

        except InvalidState as e:
            errors.append(f'Row {idx}: {str(e)}')

    return import_count, errors