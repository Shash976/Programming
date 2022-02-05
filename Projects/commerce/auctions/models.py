from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    bid = models.IntegerField()
    user = models.CharField(max_length=24)
    image=models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return f"{self.title}: ${self.bid} [Listed by: {self.user}]"

class Category(models.Model):
    category = models.CharField(max_length=64)
    listings = models.ManyToManyField(Listing, blank=True, related_name="categories")

    def __str__(self):
        return f"{self.category}"

class Bid(models.Model):
    user = models.CharField(max_length=50)
    bid = models.IntegerField()
    listing_title = models.CharField(max_length=100)

    def __str__(self):
        return f"Bid of {self.listing_title} of {self.bid} by {self.user}"