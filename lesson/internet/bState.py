from lesson.cards.defaultCard import DefaultCard
from lesson.internet.aState import AState
from lesson.internet.states import BSTATE
from lesson.lessonState import LessonState
from student.models import Student


class BState(LessonState):
    @staticmethod
    def _make_card(student: Student):
        res = AState.get_results(student)
        return DefaultCard("Danke", "Du bist toll! Auswahl: " + str(res["knowledge"]), "<3", BSTATE)

    def next_state(self, student: Student) -> int:
        return 0  # FIXME: Implement more states

    def html(self, request, student: Student) -> str:
        return self._make_card(student).get_html(request)

    def handle_post(self, post, student: Student):
        return self._make_card(student).handle_post(post, student, "INTERNET")

    @staticmethod
    def get_results(student):
        pass
