from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import CharField, ForeignKey, CASCADE, IntegerField, BooleanField

from teacher.models import Room


class Student(models.Model):
    user_name = CharField(max_length=4)
    # TODO: Don't allow null values
    session = ForeignKey(Session, on_delete=CASCADE, blank=True, null=True)
    room = ForeignKey(Room, on_delete=CASCADE)
    current_state = IntegerField(default=0)
    is_syncing = BooleanField(default=False)
