from django.db import models


# Create your models here.
class Words(models.Model):
    string = models.TextField(True)
