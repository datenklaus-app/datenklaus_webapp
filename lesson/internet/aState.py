from django.core.exceptions import ObjectDoesNotExist

from lesson.cards.rangeSelectCard import RangeSelectCard
from lesson.charts import DKBarChart
from lesson.internet.states import ASTATE, BSTATE
from lesson.lessonState import LessonState
from lesson.models import LessonSateModel
from student.models import Student


class AState(LessonState):
    card = RangeSelectCard("Wie schätzt du dein Wissen zum Thema Internet ein ?",
                           list(map(lambda x: (x, str(x + 1)), range(0, 5))), ASTATE)

    def get_state_number(self) -> int:
        return ASTATE

    def next_state(self, student: Student) -> int:
        return BSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def handle_post(self, post, student):
        result = self.card.handle_post(post)
        try:
            s = LessonSateModel.objects.get(state=ASTATE, student=student, room=student.room)
        except ObjectDoesNotExist:
            raise LessonState.LessonStateError(ASTATE)
        s.choice = result['value']
        s.save()

    @staticmethod
    def get_result(room, student) -> int:
        try:
            if student is not None:
                obj = LessonSateModel.objects.get(state=ASTATE, student=student, room=room)
                res = [int(obj.choice)]
        except (ObjectDoesNotExist, KeyError):
            raise LessonState.LessonStateError(ASTATE)

        return res

    @staticmethod
    def result_svg(room: str) -> str:
        objs = LessonSateModel.objects.filter(state=ASTATE, room=room)
        data = [0] * 5
        for o in objs:
            data[int(o.choice)] += 1

        return DKBarChart(dataset=data, labels=list(map(lambda i: str(i), range(1, 6)))).render()

    @staticmethod
    def get_name():
        return "Selbsteinschätzung"
