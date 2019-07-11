from lesson.cards.BarChartCard import LineChartCard
from lesson.internet.aState import AState
from lesson.lessonState import LessonState
from student.models import Student


class BState(LessonState):
    card = LineChartCard(list(map(lambda i: str(i), range(1, 11))), title="So schätzt ihr euch ein:")

    def next_state(self, student: Student) -> int:
        return 0  # FIXME: Implement more states

    def render(self, request, student: Student, context) -> str:
        results = AState().get_results(student.room)

        return self.card.render(request, context, dataset=results['knowledge'])

    def handle_post(self, post, student: Student):
        return None

    @staticmethod
    def get_results(room, student=None):
        pass
