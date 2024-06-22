from django.db import models

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=100, null=False)
    team_type = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.team_name