from django.db import models
import uuid

# Create your models here.

class Club(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    creation_date = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True, null=True)