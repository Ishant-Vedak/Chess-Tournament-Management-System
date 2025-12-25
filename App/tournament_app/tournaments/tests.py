from django.test import TestCase
from .models import Tournament, JoinTournament
from users.models import User
from clubs.models import Club
# Create your tests here.


class TournamentTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="DHC", email='dhc@gmail.com')
        User.objects.create(username='organizer', email = 'org@gmail.com')
        Club.objects.create(name='Sample Club')
        lead = User.objects.get(username='organizer')
        club = Club.objects.get(name='Sample Club')
        Tournament.objects.create(name='Sample Tournament', lead_organizer=lead, club=club)
    
    def testingTournament(self):
        tourney = Tournament.objects.get(name='Sample Tournament')
        self.assertEqual(tourney.details(), 'The tournament is hosted by organizer from Sample Club.')


class JoinTournamentTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="DHC", email='dhc@gmail.com')
        User.objects.create(username='organizer', email = 'org@gmail.com')
        Club.objects.create(name='Sample Club')
        lead = User.objects.get(username='organizer')
        club = Club.objects.get(name='Sample Club')
        Tournament.objects.create(name='Sample Tournament', lead_organizer=lead, club=club)

    def testingJoinTournament(self):
        participant = User.objects.get(username='DHC')
        tournament = Tournament.objects.get(name='Sample Tournament')
        new_join = JoinTournament(user=participant, tournament=tournament)
        self.assertEqual(new_join.join_statement(), 'DHC has joined Sample Tournament.')