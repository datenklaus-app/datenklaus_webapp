from django.contrib.sessions.models import Session
from django.db import models

class Room(models.Model):
    room_name = models.CharField(max_length=4096, primary_key=True)
    #module = models.CharField(max_length=4096)

    def __str__(self):
        return self.room_name
