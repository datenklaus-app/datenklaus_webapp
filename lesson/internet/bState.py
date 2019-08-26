from lesson.cards.templateCard import TemplateCard
from lesson.internet.aState import AState
from lesson.internet.states import CSTATE, BSTATE
from lesson.lessonState import LessonState
from student.models import Student


class BState(LessonState):
    card = TemplateCard(BSTATE, template="lesson/internet/b-textCard.html")

    def state_number(self) -> int:
        return BSTATE

    def next_state(self, student: Student) -> int:
        return CSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student: Student):
        pass

    @staticmethod
    def name():
        return "Internet Basics 1"
