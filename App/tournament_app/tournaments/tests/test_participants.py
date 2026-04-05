from django.test import TestCase
from users.models import User
from tournaments.models import Tournament, Participant
from tournaments.services import participants, state, swiss
from tournaments.services.state import InvalidState
import csv
import tempfile
from django.db.utils import IntegrityError

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
        with tempfile.NamedTemporaryFile(mode='wb+', delete=True) as tmp:
            content = "Name, Email, CFC Rating\n"
            for i in range(1, 11):  
                content += f"K{i},k{i}@gmail.com,{i}00\n"
            tmp.write(content.encode('utf-8'))
            tmp.seek(0)
            import_count, errors = participants.import_participants_from_csv(
                tournament=tournament,
                file=tmp
            )
            self.assertEqual(import_count, 10)
            self.assertEqual(errors, [])

            pairs = swiss.generate_swiss_pairings(tournament=tournament)
            self.assertEqual(len(pairs), 5)
    def testing_import_participants_with_wrong_format(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        with tempfile.NamedTemporaryFile(mode='wb+', delete=True) as tmp:
            content = "Email,CFC Rating\n"
            for i in range(1, 11):
                content += f"k{i}@gmail.com,{i}00\n"
            tmp.write(content.encode('utf-8'))
            tmp.seek(0)
            with self.assertRaises(IntegrityError):
                participants.import_participants_from_csv(tournament=tournament, file=tmp)

            