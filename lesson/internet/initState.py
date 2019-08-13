from lesson.cards.textCard import TextCard
from lesson.internet.states import ASTATE, INITSTATE
from lesson.lessonState import LessonState
from student.models import Student


class InitState(LessonState):
    card = TextCard("Willkommen",
                       "Heute lernen wir etwas über das Internet",
                       "Das Internet ist sehr toll", INITSTATE)

    def state_number(self):
        return INITSTATE

    def previous_state(self, student: Student):
        return None  # Initial state has no previous

    def next_state(self, student: Student) -> int:
        return ASTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        return self.card.post(post)

    @staticmethod
    def name():
        return "Intro"
