from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class Club(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=300, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name