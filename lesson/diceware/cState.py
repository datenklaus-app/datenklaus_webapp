from lesson.cards.templateCard import TemplateCard
from lesson.diceware.states import CSTATE, DSTATE
from lesson.lessonState import LessonState
from student.models import Student


class CState(LessonState):
    card = TemplateCard(template='lesson/diceware/c-textCard.html')

    def state_number(self):
        return CSTATE

    def next_state(self, student: Student) -> int:
        return DSTATE

    def render(self, request, student: Student, context: {}) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        self.card.post(post)

    @staticmethod
    def name():
        return "Zauberer Slides"
