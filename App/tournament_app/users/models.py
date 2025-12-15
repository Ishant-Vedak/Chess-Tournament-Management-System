from django.db import models
import uuid
# Create your models here.

class BaseAbstractUser(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200)
    email = models.EmailField
