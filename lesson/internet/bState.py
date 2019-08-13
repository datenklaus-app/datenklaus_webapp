from lesson.cards.chartCard import ChartCard
from lesson.internet.aState import AState
from lesson.internet.states import CSTATE, BSTATE
from lesson.lessonState import LessonState
from student.models import Student


class BState(LessonState):
    card = ChartCard(BSTATE, title="So schätzt ihr euch ein:")

    def state_number(self) -> int:
        return BSTATE

    def next_state(self, student: Student) -> int:
        return CSTATE

    def render(self, request, student: Student, context) -> str:
        chart = AState.result_svg(student.room)
        return self.card.render(request, context, chart=chart)

    def post(self, post, student: Student):
        pass

    @staticmethod
    def name():
        return "Selbsteinschätzung: Ergebnis"
