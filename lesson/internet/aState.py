from django.core.exceptions import ObjectDoesNotExist

from lesson.cards.sliderCard import SliderCard
from lesson.internet.states import ASTATE, BSTATE
from lesson.lessonState import LessonState
from lesson.models import SliderCardModel
from student.models import Student


class AState(LessonState):
    card = None

    def _make_card(self):
        return SliderCard("Wie schätzt du dein Wissen zum Thema Internet ein ?", 0, 10, ASTATE)

    def next_state(self, student: Student) -> int:
        return BSTATE

    def html(self, request, student: Student) -> str:
        return self._make_card().get_html(request)

    def handle_post(self, post, student):
        self._make_card().handle_post(post, student, "INTERNET")

    @staticmethod
    def get_results(student):
        try:
            obj = SliderCardModel.objects.get(state=ASTATE, student=student, lesson="INTERNET")
        except ObjectDoesNotExist:
            raise LessonState.LessonStateError(ASTATE)

        return {"knowledge": obj.selected_value}
