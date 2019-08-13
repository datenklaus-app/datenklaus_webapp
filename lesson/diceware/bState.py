from lesson.cards.textCard import TextCard
from lesson.diceware.states import BSTATE, CSTATE
from lesson.lessonState import LessonState
from student.models import Student


class BState(LessonState):
    card = TextCard(state=BSTATE, template="lesson/diceware/b-textCard.html")

    def state_number(self) -> int:
        return BSTATE

    def next_state(self, student: Student) -> int:
        return CSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student: Student):
        return None

    @staticmethod
    def name():
        return "Erklärung: Spielprinzip"
