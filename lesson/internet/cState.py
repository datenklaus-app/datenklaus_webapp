from lesson.cards.imageCard import ImageCard
from lesson.internet.states import CSTATE, INITSTATE
from lesson.lessonState import LessonState
from student.models import Student


class CState(LessonState):
    card = ImageCard(["/lesson/internet/anm-1.png", "/lesson/internet/anm-2.png"], CSTATE)

    def get_state_number(self):
        return CSTATE

    def next_state(self, student: Student) -> int:
        return INITSTATE

    def render(self, request, student: Student, context: {}) -> str:
        return self.card.render(request, context)

    def handle_post(self, post, student):
        self.card.handle_post(post)
