from django.db import models
import uuid
from clubs.models import Club
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Tournament(models.Model):
    UPCOMING = "UP"
    OPEN = "OP"
    ONGOING = "ON"
    CLOSED = "CL"
    Tournament_Status = {
        UPCOMING: "Upcoming",
        OPEN: "Open",
        ONGOING: "Ongoing",
        CLOSED: "Closed",
    }

    IN_PERSON = "INP"
    ONLINE = "ONL"
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

    def __str__(self):
        return self.name
    
    def organizer_details(self):
        return f"The tournament is hosted by {self.lead_organizer} from {self.club}"