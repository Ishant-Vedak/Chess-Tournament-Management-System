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
    new, created = Participant.objects.get_or_create(name=name, second_name=second_name, tournament=t, email=email, cfc_rating=cfc_rating, fide_rating=fide_rating)

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

    PARTIAL_NAME_IDENTIFIERS = {
        "cfc_rating": ["cfc", "rating"],
        "fide_rating": ["fide", "rating"],
        "name": ['name', 'first'],
        "last_name": ['last', 'name'],
        "email": ["email"]
    }

    def find_key(given_header: str):
        cleaned = given_header.lower().strip()
        for official_name, keywords in PARTIAL_NAME_IDENTIFIERS.items():
            if all(word in cleaned for word in keywords):
                return official_name
            if cleaned == 'elo': 
                return 'fide_rating'
        return cleaned.strip()
    data = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(data), skipinitialspace=True)

    for idx, row in enumerate(reader, start=1):
        new_row = {}
        for original_key, value in row.items():
            clean_key = find_key(original_key)
            clean_value = value.strip()
            new_row[clean_key] = clean_value
        try:
            add_participant(
                tournament=tournament, 
                name=new_row['name'], 
                second_name = new_row['last_name'],
                email=new_row['email'], 
                cfc_rating=int(new_row['cfc_rating']), 
                fide_rating=int(new_row['fide_rating']),

            )
            import_count += 1

        except InvalidState as e:
            errors.append(f'Row {idx}: {str(e)}')

    return import_count, errors

    # headers = [header.strip().lower() for header in reader.fieldnames]

    # if not "name" in headers:
    #     raise ValueError("CSV File is missing column 'name'. ")
    
    # aliases = {
    #     'cfc': ['cfc rating', 'cfc_rating', 'cfc', 'national rating'],
    #     'fide': ['fide rating', 'fide_rating', 'fide', 'elo']
    # }

    # for i, row in enumerate(reader, start=1):
    #     name = row.get('name', '').lower().strip()
    #     email = row.get('email', '').lower().strip() or None
    #     cfc_rating = row.get('CFC rating', '').strip() or row.get('cfc_rating', '').strip() or None
    #     fide_rating = row.get('FIDE rating', '').strip() or row.get('fide_rating', '').strip() or None

    #     if not name: 
    #         errors.append(f'Row {i}: Missing name')
    #         continue

    #     if cfc_rating is not None or fide_rating is not None:
    #         try: 
    #             cfc_rating = int(cfc_rating)
    #             fide_rating = int(fide_rating)
    #         except ValueError:
    #             errors.append(f'Invalid Rating on Row {i}')
    #             continue
    #     try: 
    #         add_participant(tournament=tournament, name=name, email=email, cfc_rating=cfc_rating, fide_rating=fide_rating)
    #         import_count += 1 
    #     except InvalidState as e:
    #         errors.append(f'Row {i}: {str(e)}')
            
    # return import_count, errors