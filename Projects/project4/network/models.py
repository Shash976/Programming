from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='media/', blank=True)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

class Post(models.Model):
    content = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='media/', blank=True)
    time = models.DateTimeField()
    likes = models.IntegerField()

    def __str__(self):
        return f"Post by {self.user} at {self.time}"    

    def serialize(self):
        return {
            "id": self.id,
            "user": {
                "username": self.user.username,
                "Name": self.user.first_name
                },
            "content": self.content,
            "likes": self.likes,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
        }