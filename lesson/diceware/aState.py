from django.core.exceptions import ObjectDoesNotExist

from lesson.cards.rangeSelectCard import RangeSelectCard
from lesson.charts import DKBarChart
from lesson.diceware.states import ASTATE, BSTATE
from lesson.lessonState import LessonState
from lesson.models import LessonSateModel
from student.models import Student


class AState(LessonState):
    _OPTIONS = [(0, "Sehr schlecht"),
                (1, "Eher schlecht"),
                (2, "Naja"),
                (3, "Eher gut"),
                (4, "Sehr gut")]

    card = RangeSelectCard("Wie schätzt du dein Wissen zum Thema Internet <nobr>ein ?</nobr>",
                           _OPTIONS, ASTATE)

    def state_number(self) -> int:
        return ASTATE

    def next_state(self, student: Student) -> int:
        return BSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        result = self.card.post(post)
        try:
            s = LessonSateModel.objects.get(state=ASTATE, student=student, room=student.room)
        except ObjectDoesNotExist:
            raise LessonState.LessonStateError(ASTATE)
        s.choice = result['value']
        s.save()

    @staticmethod
    def result(room, student) -> int:
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

        return DKBarChart(dataset=data, labels=list(map(lambda x: x[1], AState._OPTIONS))).render(
            disable_xml_declaration=True)

    @staticmethod
    def name():
        return "Selbsteinschätzung"
