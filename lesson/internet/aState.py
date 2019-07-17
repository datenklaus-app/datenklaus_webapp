from django.core.exceptions import ObjectDoesNotExist

from lesson.cards.sliderCard import SliderCard
from lesson.internet.states import ASTATE, BSTATE
from lesson.lessonState import LessonState
from lesson.models import SliderCardModel
from student.models import Student


class AState(LessonState):
    card = SliderCard("Wie schätzt du dein Wissen zum Thema Internet ein ?", 0, 9, ASTATE)

    def next_state(self, student: Student) -> int:
        return BSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def handle_post(self, post, student):
        self.card.handle_post(post, student)

    @staticmethod
    def get_results(room, student=None):
        """
        :param room:
        :param student:
        :return: A list of results for the entire room (or a students individual result) as list
        """
        try:
            if student is not None:
                obj = SliderCardModel.objects.get(state=ASTATE, student=student, room=room)
                res = [obj.selected_value]
            else:
                objs = SliderCardModel.objects.filter(state=ASTATE, room=room)
                res = [0]*10
                for o in objs:
                    res[o.selected_value] += 1

        except ObjectDoesNotExist:
            raise LessonState.LessonStateError(ASTATE)

        return {"knowledge": res}
