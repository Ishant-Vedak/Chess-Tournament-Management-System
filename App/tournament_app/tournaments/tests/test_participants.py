from django.test import TestCase
from users.models import User
from tournaments.models import Tournament, Participant
from tournaments.services import participants, state
from tournaments.services.state import InvalidState

class ParticipantTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="T. Scott", email='wiggly@wobbly.com')
        org = User.objects.get(username='T. Scott')
        Tournament.objects.create(name='WigglyWobbly', lead_organizer=org)
    def testing_add_participants_with_open_reg(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        participants.add_participant(t=tournament, name="Challenger")
        participant = Participant.objects.get(name="Challenger")
        self.assertEqual(str(participant), "Challenger in WigglyWobbly.")
    def testing_add_participants_with_closed_reg(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        state.close_registration(tournament)
        with self.assertRaises(InvalidState):
            participants.add_participant(t=tournament, name='Challenger2')
