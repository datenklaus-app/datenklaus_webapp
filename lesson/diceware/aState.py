from lesson.cards.textCard import TextCard
from lesson.diceware.states import ASTATE, BSTATE
from lesson.lessonState import LessonState
from student.models import Student


class AState(LessonState):
    card = TextCard(None, None, None, ASTATE, template="lesson/diceware/a-textCard.html")

    def state_number(self) -> int:
        return ASTATE

    def next_state(self, student: Student) -> int:
        return BSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        return None

    @staticmethod
    def name():
        return "Hinführung zum Spiel"
