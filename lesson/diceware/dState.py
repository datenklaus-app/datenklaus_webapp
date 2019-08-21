from lesson.cards.textCard import TextCard
from lesson.diceware.states import DSTATE, ESTATE
from lesson.lessonState import LessonState
from student.models import Student


class DState(LessonState):
    card = TextCard(DSTATE, template='lesson/diceware/d-diceGameCard.html')

    def state_number(self):
        return DSTATE

    def next_state(self, student: Student) -> int:
        return ESTATE

    def render(self, request, student: Student, context: {}) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        self.card.post(post)

    @staticmethod
    def name():
        return "Zauberer Slides"
