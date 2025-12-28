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
    
    def testingOverallCount_1(self):
        user = User.objects.get(username='DHC')
        tournament = Tournament.objects.get(name='Sample Tournament')
        new = JoinTournament(user=user, tournament=tournament)
        new.save()
        self.assertEqual(tournament.overall_count(), 'There is 1 person in this tournament overall.')

    def testingOverallCount_Many(self):
        user1 = User.objects.get(username='DHC')
        user2 = User.objects.get(username='organizer')
        tournament = Tournament.objects.get(name='Sample Tournament')
        new1 = JoinTournament(user=user1, tournament=tournament)
        new1.save()
        new2 = JoinTournament(user=user2, tournament=tournament)
        new2.save()
        self.assertEqual(tournament.overall_count(), 'There are 2 people in this tournament overall.')


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
        self.assertEqual(new_join.join_details(), 'DHC has joined Sample Tournament.')
        self.assertEqual(new_join.role, "PARTICIPANT")