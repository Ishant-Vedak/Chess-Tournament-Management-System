from django.db import models
import uuid
from users.models import User
from clubs.models import Club
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Tournament(models.Model):
    DRAFT = "DRAFT"
    REGISTRATION_OPEN = "REGISTRATION_OPEN"
    REGISTRATION_CLOSED = "REGISTRATION_CLOSED"
    ONGOING = "ONGOING"
    CLOSED = "CLOSED"
    Tournament_Status = {
        DRAFT: "Draft",
        REGISTRATION_OPEN: "Registration_Open",
        REGISTRATION_CLOSED: "Registration_Closed",
        ONGOING: "Ongoing",
        CLOSED: "Closed",
    }

    IN_PERSON = "IN_PERSON"
    ONLINE = "ONLINE"
    Tournament_Type = {
        IN_PERSON: "In_Person",
        ONLINE: "Online",
    }

    SWISS = "SWISS"
    ROUND_ROBIN = "ROUND_ROBIN"
    KNOCKOUT = "KNOCKOUT"
    DOUBLE_ELIMINATION = "DOUBLE_ELIMINATION" #Advanced, maybe for the future.
    Tournament_Format = {
        SWISS: "Swiss",
        ROUND_ROBIN: "Round_Robin",
        KNOCKOUT: "Knockout",
        DOUBLE_ELIMINATION: "Double_Elimination"
    }

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=300)
    creation_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=Tournament_Status, default=DRAFT)
    type = models.CharField(max_length=100, choices=Tournament_Type, default=IN_PERSON)
    format = models.CharField(max_length=100, choices=Tournament_Format, default=SWISS)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    lead_organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='JoinTournament', related_name='tournaments')
    rounds = models.IntegerField(default=0)

    class Meta:
        get_latest_by = 'creation_date'
    
    def __str__(self):
        return self.name
    
    def details(self):
        return f"The tournament is hosted by {self.lead_organizer} from {self.club}."
    
    def overall_count(self):
        count = self.participants.count()
        if count == 1:
            return f'There is 1 person in this tournament overall.'
        return f'There are {count} people in this tournament overall.'
    


class JoinTournament(models.Model):
    '''
    This model is for adding people to tournaments, either as a participant, an admin or an organizer. 
    '''
    ORGANIZER = "ORGANIZER"
    ADMIN = "ADMIN"
    PARTICIPANT = "PARTICIPANT"
    Roles = {
        ORGANIZER: "Organizer",
        ADMIN: "Admin",
        PARTICIPANT: "Participant",
    }
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="joined_tournaments")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="people_joined")
    role = models.CharField(max_length=12, choices=Roles, default=PARTICIPANT)
    join_date = models.DateTimeField(default=timezone.now)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tournament'],
                name= 'unique_user_tournament_enrolment'
            )
        ]

    def __str__(self):
        return f'{self.user} in {self.tournament}'

    def join_details(self):
        return f"{self.user} has joined {self.tournament}."

class Participant(models.Model):
    '''
    This model is for a Participant in a tournament. It other than a name, it has a random seed (used for creating pairings), rating, email and points. 
    '''
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=150)
    random_seed = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    points = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tournament'],
                name= 'unique_tournament_participant'
            )
        ]

    def __str__(self):
        return f'{self.name} in {self.tournament}.'
    
class HostTournament(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tournament = models.OneToOneField(
        Tournament, 
        on_delete=models.CASCADE,
        related_name='host'
    )
    total_rounds = models.IntegerField(default=0)
    current_round = models.IntegerField(default=0)
    round_is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'Hosting model for {self.tournament}.'

class Match(models.Model):
    '''
    This model is for a match between two players in a round. It will use a tournament from Tournament model for identification and filtering, and a round number to specifiy the round in the tournament. Then it will take two Participant models, found using p1 and p2, to create a match between two players. 
    Main purpose is to keep the same pairings for a round regardless of the page being refreshed. 
    '''
    WIN = "WIN"
    DRAW = "DRAW"
    LOSS = "LOSS"
    Results = {
       WIN: 'Win',
       DRAW: 'Draw',
       LOSS: 'Loss',
    }

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round_num = models.IntegerField(default=0)
    player_1 = models.ForeignKey(Participant, related_name='p1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Participant, related_name='p2', on_delete=models.CASCADE)
    p1_result = models.CharField(max_length=4, choices=Results, default=DRAW)