from django.db import models
from authApp import models as authDb
import uuid

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=100, null=False)
    team_type = models.CharField(max_length=100, null=False)
    team_leader = models.CharField(max_length=500, unique=False, blank=False, null=False)
    accessToken = models.CharField(max_length=1000, unique=True, blank=False, null=False)

    def __str__(self):
        return self.team_name