from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from .convert import *

# Create your models here.
class User(AbstractUser):
    pass


class Mail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mails")
    file = models.FileField(upload_to="media/", blank=False, validators=[FileExtensionValidator(allowed_extensions=['json', 'xlsx', 'csv'])])
    json_file = models.FileField(upload_to="media/json/", blank=True, validators=[FileExtensionValidator(allowed_extensions=['json'])])
    body = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.file.name[self.file.name.rindex('/') + 1:]}"
