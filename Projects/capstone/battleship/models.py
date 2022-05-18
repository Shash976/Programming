from django.db import models
from django.contrib.auth.models import AbstractUser
import json


# Create your models here.
class User(AbstractUser):
    hits = models.IntegerField(default=0)
    turns = models.IntegerField(default=0)
