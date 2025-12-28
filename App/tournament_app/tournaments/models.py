from django.db import models
import uuid
from clubs.models import Club
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Tournament(models.Model):
    UPCOMING = "UPCOMING"
    OPEN = "OPEN"
    ONGOING = "ONGOING"
    CLOSED = "CLOSED"
    Tournament_Status = {
        UPCOMING: "Upcoming",
        OPEN: "Open",
        ONGOING: "Ongoing",
        CLOSED: "Closed",
    }

    IN_PERSON = "IN_PERSON"
    ONLINE = "ONLINE"
    Tournament_Type = {
        IN_PERSON: "In_Person",
        ONLINE: "Online",
    }

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=300)
    creation_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=Tournament_Status, default=UPCOMING)
    type = models.CharField(max_length=100, choices=Tournament_Type, default=IN_PERSON)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    lead_organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='JoinTournament', related_name='tournaments')

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
    EXECUTIVE = "EXECUTIVE"
    PARTICIPANT = "PARTICIPANT"
    Roles = {
        ORGANIZER: "Organizer",
        EXECUTIVE: "Executive",
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
    
    