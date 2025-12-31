from django.test import TestCase
from tournaments.models import Tournament
from tournaments.services import state
from users.models import User

class StateTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test_organizer', email='organizer@test.com')
        lead = User.objects.get(username='test_organizer')
        Tournament.objects.create(name='The Test Tourney', lead_organizer=lead)

    def testing_open_reg(self):
        t = Tournament.objects.get(name='The Test Tourney')
        updated = state.open_registration(t)
        self.assertEqual(updated.status, "REGISTRATION_OPEN")
        t.refresh_from_db()
        self.assertEqual(t.status, "REGISTRATION_OPEN")

    def testing_close_reg(self):
        t = Tournament.objects.get(name='The Test Tourney')
        state.open_registration(t)
        close = state.close_registration(t)
        self.assertEqual(close.status, "REGISTRATION_CLOSED")

    def testing_start_tournament(self):
        t = Tournament.objects.get(name='The Test Tourney')
        state.open_registration(t)
        state.close_registration(t)
        start = state.start_tournament(t)
        self.assertEqual(start.status, "ONGOING")

    def testing_end_tournament(self):
        t = Tournament.objects.get(name='The Test Tourney')
        state.open_registration(t)
        state.close_registration(t)
        state.start_tournament(t)
        finish = state.end_tournament(t)
        self.assertEqual(finish.status, "CLOSED")
