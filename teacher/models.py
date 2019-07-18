from django.contrib.sessions.models import Session
from django.db import models


class Room(models.Model):
    WAITING = 0
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3
    room_name = models.CharField(max_length=4096, primary_key=True)
    module = models.CharField(max_length=4096)
    state = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.room_name
