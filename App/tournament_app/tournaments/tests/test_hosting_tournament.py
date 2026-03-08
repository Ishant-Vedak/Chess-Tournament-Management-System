from django.test import TestCase
from users.models import User
from tournaments.models import Tournament, Participant, HostTournament, Match,Round
from tournaments.services import participants, state, rounds
from tournaments.services.state import InvalidState
import csv
import tempfile

class HostingTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="T. Scott", email='wiggly@wobbly.com')
        org = User.objects.get(username='T. Scott')
        Tournament.objects.create(name='WigglyWobbly', lead_organizer=org)
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=True) as tmp:
            fieldnames = ['name', 'email']
            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'name': 'T1', 'email': 't1@gmail.com'})
            writer.writerow({'name': 'T2', 'email': 't2@gmail.com'})
            writer.writerow({'name': 'T3', 'email': 't3@gmail.com'})
            writer.writerow({'name': 'T4', 'email': 't4@gmail.com'})
            writer.writerow({'name': 'T5', 'email': 't5@gmail.com'})
            writer.writerow({'name': 'T6', 'email': 't6@gmail.com'})
            writer.writerow({'name': 'T7', 'email': 't7@gmail.com'})
            writer.writerow({'name': 'T8', 'email': 't8@gmail.com'})
            tmp.seek(0)
            participants.import_participants_from_csv(
                tournament=tournament,
                file=tmp
            )
    def testing_HostTournament_model(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        tournament.rounds = rounds.generate_total_number_of_rounds(tournament=tournament)
        tournament.save()
        self.assertEqual(tournament.rounds, 5)
        hosting = HostTournament.objects.create(tournament=tournament, total_rounds = tournament.rounds)
        self.assertEqual(hosting.total_rounds, 5)
        self.assertFalse(hosting.round_is_active)
        rounds.start_round(tournament=tournament)
        hosting.refresh_from_db()
        self.assertTrue(hosting.round_is_active)
        self.assertEqual(hosting.current_round, 1)

    def testing_generate_pairings(self):
        tournament=Tournament.objects.get(name='WigglyWobbly')
        pairs = rounds.generate_pairings(tournament=tournament)
        players = [p for pair in pairs for p in pair]
        self.assertEqual(len(pairs), 4)
        self.assertEqual(len(players), Participant.objects.filter(tournament=tournament).count())
        self.assertEqual(len(players), len(set(players)))
        for a,b in pairs:
            self.assertNotEqual(a,b)


class SecondHostingTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="T. Scott", email='wiggly@wobbly.com')
        org = User.objects.get(username='T. Scott')
        Tournament.objects.create(name='WigglyWobbly', lead_organizer=org)
        tournament=Tournament.objects.get(name='WigglyWobbly')
        state.open_registration(tournament)
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=True) as tmp:
            fieldnames = ['name', 'email']
            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'name': 'T1', 'email': 't1@gmail.com'})
            writer.writerow({'name': 'T2', 'email': 't2@gmail.com'})
            writer.writerow({'name': 'T3', 'email': 't3@gmail.com'})
            writer.writerow({'name': 'T4', 'email': 't4@gmail.com'})
            writer.writerow({'name': 'T5', 'email': 't5@gmail.com'})
            writer.writerow({'name': 'T6', 'email': 't6@gmail.com'})
            writer.writerow({'name': 'T7', 'email': 't7@gmail.com'})
            tmp.seek(0)
            participants.import_participants_from_csv(
                tournament=tournament,
                file=tmp
            )

    def testing_generate_pairing_with_odd_players(self):
        tournament = Tournament.objects.get(name='WigglyWobbly')
        pairs = rounds.generate_pairings(tournament=tournament)
        total_participants = Participant.objects.filter(tournament=tournament)
        self.assertEqual(len(total_participants), 8)
        self.assertEqual(len(pairs), 4)

        r1 = Round.objects.create(tournament=tournament, round_num = 1)
        for pair in pairs:
            Match.objects.create(
                tournament=tournament,
                round_model = r1,
                round_num = 1,
                player_1 = pair[0],
                player_2 = pair[1],

            )
            ping = rounds.derive_points(tournament=tournament, player=pair[0])
            self.assertEqual(ping, 0)