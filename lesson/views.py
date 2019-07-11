# Create your views here.
from chartjs.colors import next_color
from chartjs.views.lines import BaseLineChartView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from lesson.internet.internet import Internet
from lesson.lessonState import LessonState
from student.models import Student


def get_state(lesson_name, state):
    if lesson_name == "INTERNET":
        return Internet.get_state(state)
    raise NotImplementedError("Selected Lesson does not exist")


def get_lessons_list():
    return ["INTERNET"]


def get_lessons_description(lesson):
    return "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt."


def lesson(request, state_num=None):
    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/")

    if state_num is not None:
        student.current_state = state_num
    current_lesson = student.room.module

    try:
        state = get_state(current_lesson, student.current_state)

        if request.method == 'POST':
            state.handle_post(request.POST, student)
            student.current_state = state.next_state(student)
            student.save()
            return HttpResponseRedirect(reverse("lesson", args=[student.current_state]))
        else:  # FIXME: Handle potential error cases?
            pass  # Resend current card  if we receive a GET request
    except LessonState.LessonStateError as e:
        return HttpResponseRedirect(reverse("lesson", args=[e.fallback_state]))

    context = {"rname": student.room}
    return state.render(request, student, context)


class LineChartJSONView(BaseLineChartView):
    COLORS = [(122, 159, 191)]

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["0", "1", "2", "3", "4", "5", "6", "7", "8"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Ergebnisse"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[0, 2, 1, 5, 6, 5, 1, 2, 0]]

    def get_colors(self):
        return next_color(color_list=self.COLORS)


def chart(request):
    view = LineChartJSONView()
    context = {"data": view.convert_context_to_json(view.get_context_data())}
    return render(request, 'lessons/cards/barChartCard.html', context=context)
