from django.contrib.sessions.models import Session
from django.db import models

from teacher.constants import RoomStates


class Room(models.Model):
    room_name = models.CharField(max_length=4096, primary_key=True)
    lesson = models.CharField(max_length=4096)
    password = models.CharField(max_length=10)
    state = models.SmallIntegerField(default=RoomStates.WAITING.value)

    def __str__(self):
        return self.room_name
