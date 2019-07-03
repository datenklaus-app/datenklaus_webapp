from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import CharField, ForeignKey, CASCADE, IntegerField

from teacher.models import Room


class Student(models.Model):
    user_name = CharField(max_length=4)
    session = ForeignKey(Session, on_delete=CASCADE)
    room = ForeignKey(Room, on_delete=CASCADE)
    current_state = IntegerField()


class CardState(models.Model):
    student = ForeignKey(Student, on_delete=CASCADE)
    lesson = CharField(max_length=2048)
    state = IntegerField()
    card = models.TextField()
