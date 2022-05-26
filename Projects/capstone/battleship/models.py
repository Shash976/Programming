from django.db import models
from django.contrib.auth.models import AbstractUser

import json
import inflect


# Create your models here.
class User(AbstractUser):
    hits = models.IntegerField(default=0)
    turns = models.IntegerField(default=0)

class Map(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maps")
    map = models.CharField(max_length=41, default="[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]")

    def serialize(self):
        return {
            "user": self.user.username,
            "map" : json.loads(self.map)
        }

class Match(models.Model):
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_player1")
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_player2")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_won")

    
    class Meta:
        verbose_name_plural = "Matches"