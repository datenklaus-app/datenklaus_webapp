# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
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
    current_lesson = student.room.lesson

    try:
        state = get_state(current_lesson, student.current_state)

        if request.method == 'POST':
            # FIXME : clean up this mess!
            state.handle_post(request.POST, student)
            student.current_state = state.next_state(student)
            state = get_state(current_lesson, student.current_state)
            state.set_previous_state(student, state_num)
            student.save()
            return HttpResponseRedirect(reverse("lesson", args=[student.current_state]))
        else:  # FIXME: Handle potential error cases?
            student.save()  # Resend current card  if we receive a GET request
    except LessonState.LessonStateError as e:
        return HttpResponseRedirect(reverse("lesson", args=[e.fallback_state]))

    context = {"lname": student.room.lesson, "rname": student.room, "previous_state": state.get_previous_state(student)}
    return state.render(request, student, context)
