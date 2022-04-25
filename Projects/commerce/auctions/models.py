from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    test = models.TextField(blank=True)

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    base_price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    image = models.ImageField(upload_to='media/', blank=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidded_on")
    bid = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.title}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.user}\'s Watchlist [{len(self.listings.all())} listing(s)]"

class Category(models.Model):
    category = models.CharField(max_length=20)
    listings = models.ManyToManyField(Listing, related_name="categories", blank=True)

    def __str__(self):
        return f"{self.category}"

    class Meta:
        verbose_name_plural = "categories"

class Bid(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")
    bid = models.IntegerField()