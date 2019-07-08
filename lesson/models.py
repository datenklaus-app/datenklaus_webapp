from django.db import models

# Create your models here.
from django.db.models import CASCADE

from student.models import Student


class SliderCardModel(models.Model):
    student = models.ForeignKey(Student, on_delete=CASCADE)
    lesson = models.CharField(max_length=2048)
    state = models.IntegerField()
    selected_value = models.IntegerField(null=True)
