from lesson.cards.defaultCard import DefaultCard
from lesson.internet.states import ASTATE, INITSTATE
from lesson.lessonState import LessonState
from student.models import Student


class InitState(LessonState):
    @staticmethod
    def _make_card():
        return DefaultCard("Willkommen",
                           "Heute lernen wir etwas über das Internet",
                           "Das Internet ist sehr toll", INITSTATE)

    def next_state(self, student: Student) -> int:
        return ASTATE

    def html(self, request, student: Student) -> str:
        return self._make_card().get_html(request)

    def handle_post(self, post, student):
        return self._make_card().handle_post(post, student, "INTERNET")

    def get_results(self, student):
        pass  # FIXME: Maybe add a check to see whether this state has already been executed by the student once
