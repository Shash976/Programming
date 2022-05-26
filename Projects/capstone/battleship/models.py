from django.db import models
from django.contrib.auth.models import AbstractUser

import json
import inflect


# Create your models here.
class User(AbstractUser):
    pass

class Map(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maps")
    map = models.CharField(max_length=41, default="[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]")

    def serialize(self):
        return {
            "user": self.user.username,
            "map" : json.loads(self.map)
        }
    
    def __str__(self):
        x = inflect.engine()
        return f"{self.user}\'s {x.number_to_words(x.ordinal(list(self.user.maps.all()).index(self)+1)).capitalize()} Map"

class Match(models.Model):
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_player1")
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_player2")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_won")

    
    class Meta:
        verbose_name_plural = "Matches"