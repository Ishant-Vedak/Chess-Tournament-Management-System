from django.db import models
import uuid
from clubs.models import Club

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

    IN_PERSON = "InP"
    ONLINE = "ONL"
    Tournament_Type = {
        IN_PERSON: "In Person",
        ONLINE: "Online",
    }

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    creation_date = models.DateTimeField
    status = models.CharField(max_length=100, choices=Tournament_Status, default=UPCOMING)
    type = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)