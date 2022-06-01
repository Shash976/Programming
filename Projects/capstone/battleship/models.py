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

    def serialize(self):
        return {
            "id" : self.id,
            "players": [PlayerInGame.objects.get(user=user, match=self).serialize() for user in self.players.all()]
        }

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
    map = models.CharField(max_length=56, default=json.dumps([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
    inGameMap = models.CharField(max_length=56, blank=True)
    turns = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.inGameMap == None:
            self.inGameMap = self.map
        super(PlayerInGame, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "InGame Players"
    
    def __str__(self):
        return f"Player - {self.user} in game {self.match.id}"
