from django.core.exceptions import ObjectDoesNotExist

from lesson.cards.rangeSelectCard import RangeSelectCard
from lesson.cards.templateCard import TemplateCard
from lesson.charts import DKBarChart
from lesson.internet.states import ASTATE, BSTATE
from lesson.lessonState import LessonState
from lesson.models import LessonSateModel
from student.models import Student
from teacher.models import Room


class AState(LessonState):

    card = TemplateCard(ASTATE, template="lesson/internet/a-textCard.html")

    def state_number(self) -> int:
        return ASTATE

    def next_state(self, student: Student) -> int:
        return BSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        return

    @staticmethod
    def name():
        return "Hinführung"
