from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from lesson.charts import DKBarChart
from lesson.forms import RangeSelectForm
from lesson.lessonState import LessonState
from lesson.models import LessonStateModel
from lesson.templateState import TemplateState
from student.models import Student


class RangeSelectState(LessonState):
    def __init__(self, template, state, next_state, description, choices, is_first=False, is_final=False,
                 is_sync=False):
        self.__template = template
        self.__description = description
        self.__state = state
        self.__next_state = next_state
        self.__is_first = is_first
        self.__is_sync = is_sync
        self.__is_final = is_final
        self.__choices = []
        for i in range(len(choices)):
            self.__choices.append((i, choices[i]))

    def previous_state(self, student: Student):
        if self.__is_first or self.__is_sync:
            return None
        return super(RangeSelectState, self).previous_state(student)

    def is_first(self) -> bool:
        return self.__is_first

    def is_sync(self) -> bool:
        return self.__is_sync

    def is_final(self) -> bool:
        return self.__is_final

    def state_number(self) -> int:
        return self.__state

    def next_state(self, student: Student) -> int:
        return self.__next_state

    def render(self, request, student: Student, context) -> str:

        form = RangeSelectForm(self.__choices)
        context["form"] = form
        return render(request, self.__template, context=context)

    def post(self, post, student):
        try:
            s = LessonStateModel.objects.get(state=self.__state, student=student, room=student.room)
        except ObjectDoesNotExist:
            assert False

        form = RangeSelectForm(self.__choices, post=post)

        if not form.is_valid():
            raise LessonState.LessonStateError("Invalid Form")

        result = form.cleaned_data['value']
        s.choice = result
        s.save()

    def name(self):
        return self.__description

    def result_svg(self, room: str) -> str:
        objs = LessonStateModel.objects.filter(state=self.__state, room=room)
        data = [0] * len(self.__choices)
        for o in objs:
            if o.choice is None:
                continue
            data[int(o.choice)] += 1

        return DKBarChart(dataset=data, labels=list(map(lambda x: x[1], self.__choices))).render(
            disable_xml_declaration=True)
