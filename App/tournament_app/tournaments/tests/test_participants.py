from django.test import TestCase
from users.models import User
from tournaments.models import Tournament, Participant
from tournaments.services import participants, state
from tournaments.services.state import InvalidState
import csv
import tempfile

class ParticipantTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="T. Scott", email='wiggly@wobbly.com')
        org = User.objects.get(username='T. Scott')
        Tournament.objects.create(name='WigglyWobbly', lead_organizer=org)
    def testing_add_participants_with_open_reg(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        participants.add_participant(tournament=tournament, name="Challenger")
        participant = Participant.objects.get(name="Challenger")
        self.assertEqual(str(participant), "Challenger in WigglyWobbly.")
    def testing_add_participants_with_closed_reg(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        state.close_registration(tournament)
        with self.assertRaises(InvalidState):
            participants.add_participant(tournament=tournament, name='Challenger2')
    def testing_import_participants_with_correct_format(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=True) as tmp:
            fieldnames = ['name', 'email']
            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'name': 'Dane', 'email': 'Sperling'})
            writer.writerow({'name': 'Ryder', 'email': 'Hsu'})
            writer.writerow({'name': 'Hudson', 'email': 'Regis'})
            tmp.seek(0)
            import_count, errors = participants.import_participants_from_csv(
                tournament=tournament,
                file=tmp
            )
            self.assertEqual(import_count, 3)
            self.assertEqual(errors, [])
    def testing_import_participants_with_wrong_format(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=True) as tmp:
            fieldnames = ['email', 'rating']
            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'email': 'ds@gmail.com', 'rating': 2000})
            writer.writerow({'email': 'rh@gmail.com', 'rating': 2001})
            writer.writerow({'email': 'hr@gmail.com', 'rating': 9000})
            tmp.seek(0)
            with self.assertRaises(ValueError):
                participants.import_participants_from_csv(tournament=tournament, file=tmp)

            