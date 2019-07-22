from django.core.exceptions import ObjectDoesNotExist

from lesson.cards.rangeSelectCard import RangeSelectCard
from lesson.internet.states import ASTATE, BSTATE
from lesson.lessonState import LessonState
from lesson.models import LessonSateModel
from student.models import Student


class AState(LessonState):
    def get_state_number(self):
        return ASTATE

    card = RangeSelectCard("Wie schätzt du dein Wissen zum Thema Internet ein ?",
                           list(map(lambda x: (x, str(x + 1)), range(0,5))), ASTATE)

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
    def get_results(room, student=None):
        """
        :param room: Specifies the room which the results relate to
        :param student: (optional) If specified returns the result for given student
        :return: A list of results for the entire room (or a students individual result) as list
        """
        try:
            if student is not None:
                obj = LessonSateModel.objects.get(state=ASTATE, student=student, room=room)
                res = [int(obj.choice)]
            else:
                objs = LessonSateModel.objects.filter(state=ASTATE, room=room)
                res = [0] * 5
                for o in objs:
                    res[int(o.choice)] += 1

        except (ObjectDoesNotExist, KeyError):
            raise LessonState.LessonStateError(ASTATE)

        return {"knowledge": res}
