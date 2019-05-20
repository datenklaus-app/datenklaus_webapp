from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import CASCADE, ForeignKey, CharField


class Room(models.Model):
    room_name = models.CharField(max_length=4096, primary_key=True)

    def __str__(self):
        return self.room_name


class Client(models.Model):
    user_name = CharField(max_length=4)
    session = ForeignKey(Session, on_delete=CASCADE)
    room = ForeignKey(Room, on_delete=CASCADE)
