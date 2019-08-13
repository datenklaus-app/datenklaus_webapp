from django.templatetags.static import static

from lesson.cards.imageCard import ImageCard
from lesson.diceware.states import INITSTATE, ASTATE
from lesson.lessonState import LessonState
from student.models import Student


class InitState(LessonState):
    card = ImageCard(title="Sicheres Passwort", images=['lesson/diceware/dice-magician.png'], state=INITSTATE)

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
