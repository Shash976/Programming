from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    image=models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return f"{self.title}: ${self.bid} [Listed by: {self.user}]"

class Category(models.Model):
    category = models.CharField(max_length=64)
    listings = models.ManyToManyField(Listing, related_name="categories")

    def __str__(self):
        return f"{self.category}"

