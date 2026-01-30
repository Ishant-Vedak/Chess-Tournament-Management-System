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
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    total_rounds = models.IntegerField()
    current_round = models.IntegerField()

    def __str__(self):
        return f'Hosting model for {self.tournament}.'