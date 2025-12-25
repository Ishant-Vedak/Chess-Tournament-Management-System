from django.test import TestCase
from users.models import User
from .models import Club, ClubMembership

# Create your tests here.

class ClubTestCase(TestCase):
    def setUp(self):
        Club.objects.create(name='Sample Club')

    def testing_club(self):
        club = Club.objects.get(name='Sample Club')
        self.assertEqual(club.details(), 'The club is called "Sample Club" and has no website.')

class ClubMembershipTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="DHC", email='dhc@gmail.com')
        User.objects.create(username='organizer', email = 'org@gmail.com')
        Club.objects.create(name='Sample Club')
    def testing_clubmembership(self):
        user1 = User.objects.get(username = 'DHC')
        user2 = User.objects.get(username = 'organizer')
        club = Club.objects.get(name='Sample Club')
        member1 = ClubMembership(user=user1, club=club)
        member2 = ClubMembership(user=user2, club=club)
        self.assertEqual(member1.member_joined(), 'DHC has joined Sample Club.')
        self.assertEqual(member2.member_joined(), 'organizer has joined Sample Club.')