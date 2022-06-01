from django.db import models
from django.contrib.auth.models import AbstractUser

import json
import inflect


# Create your models here.
class User(AbstractUser):
    pass


class Match(models.Model):
    players = models.ManyToManyField(
        User,
        through='PlayerInGame',
        through_fields=('match', 'user'),
        related_name="matches",
    )
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_won", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Matches"
    
    def __str__(self):
        return f"Match {self.id}"

class PlayerInGame(models.Model):
    WINNER = 'Winner'
    LOSER = 'Loser'
    UKNOWN = 'Unknown'
    PLAYER_TYPE_CHOICES = [
           (WINNER, 'Winner'),
           (LOSER, 'Loser'),
           (UKNOWN, 'Unknown')
       ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    type = models.CharField(choices=PLAYER_TYPE_CHOICES, max_length=7, default=UKNOWN)
    turns = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "InGame Players"
    
    def __str__(self):
        return f"Player - {self.user} in game {self.match.id}"
