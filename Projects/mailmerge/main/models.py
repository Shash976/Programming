from django.db import models

# Create your models here.
class Recipient(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=500, blank=True)

    def __str__(self) -> str:
        return f"{self.email} - {self.first_name}"

class CSV(models.Model):
    csv_file = models.FileField(upload_to="media/")
    date_uploaded = models.DateTimeField(auto_now=True)