from lesson.cards.templateCard import TemplateCard
from lesson.diceware.states import INITSTATE, ESTATE
from lesson.lessonState import LessonState
from student.models import Student


class EState(LessonState):
    card = TemplateCard(ESTATE, template='lesson/diceware/e-textCard.html')

    def state_number(self):
        return ESTATE

    def next_state(self, student: Student) -> int:
        return INITSTATE

    def render(self, request, student: Student, context: {}) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        self.card.post(post)

    @staticmethod
    def name():
        return "Zauberer Slides"
