from django.test import TestCase
from users.models import User
from .models import Club, ClubMembership

# Create your tests here.

class ClubTestCase(TestCase):
    def setUp(self):
        Club.objects.create(name='Sample Club')
        User.objects.create(username="DHC", email='dhc@gmail.com')
        User.objects.create(username='organizer', email = 'org@gmail.com')

    def testing_club(self):
        club = Club.objects.get(name='Sample Club')
        self.assertEqual(club.details(), 'The club is called "Sample Club" and has no website.')

    def testingMemberCount_1(self):
        club = Club.objects.get(name='Sample Club')
        user = User.objects.get(username='DHC')
        new = ClubMembership(user=user, club=club)
        new.save()
        self.assertEqual(club.member_count(), 'There is 1 member.')

    def testingMemberCount_Many(self):
        club = Club.objects.get(name='Sample Club')
        user1 = User.objects.get(username='DHC')
        user2 = User.objects.get(username='organizer')
        new1 = ClubMembership(user=user1, club=club)
        new1.save()
        new2 = ClubMembership(user=user2, club=club)
        new2.save()
        self.assertEqual(club.member_count(), 'There are 2 members.')

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
        self.assertEqual(member1.join_details(), 'DHC has joined Sample Club.')
        self.assertEqual(member1.role, "MEMBER")
        self.assertEqual(member2.join_details(), 'organizer has joined Sample Club.')
        self.assertEqual(member2.role, "MEMBER")