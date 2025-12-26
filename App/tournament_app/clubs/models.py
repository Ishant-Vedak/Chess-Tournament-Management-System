from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Club(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=300, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)
    website = models.URLField(blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ClubMembership", related_name="clubs" )

    def __str__(self):
        return self.name
    
    def details(self):
        if not self.website:
            return f'The club is called "{self.name}" and has no website.'
        return f'The club is called "{self.name}" and its website is {self.website}.'
    
    def member_count(self):
        specific_club = Club.objects.get(name=self.name)
        count = list(ClubMembership.objects.filter(club=specific_club))
        if len(count) == 1:
            return f'There is 1 member.'
        return f'There are {len(count)} members.'
    

class ClubMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="club_memberships")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    join_date = models.DateTimeField(default=timezone.now)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'club'],
                name= 'unique_user_club_membership'
            )
        ]

    def __str__(self):
        return f'for {self.club}'

    def join_details(self):
        return f'{self.user} has joined {self.club}.'