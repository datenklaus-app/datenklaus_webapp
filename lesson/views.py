# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render

from lesson.lessons.cardJsonParser import from_json
from lesson.lessons.internet import Internet
from student.models import Student, CardState

STATE_INITIAL = 0


def get_initial(lesson_name):
    if lesson_name == "INTERNET":
        return Internet.initial()
    raise NotImplementedError("Selected Lesson does not exist")


def get_content(lesson_name, state, arguments):
    if lesson_name == "INTERNET":
        return Internet.next(state, arguments)
    raise NotImplementedError("Selected Lesson does not exist")


def get_lessons_list():
    return ["INTERNET"]


def get_lessons_description(lesson):
    return "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt."


def lesson(request):
    student = Student.objects.get(session=request.session.session_key)
    if student is None:
        return HttpResponseNotFound("Student has not joined a room yet")

    context = {"rname": student.room}

    current_lesson = student.room.module
    try:
        card_obj = CardState.objects.get(student=student, state=student.current_state, lesson=current_lesson)
        card = from_json(card_obj.card)
        if len(request.POST) != 0:
            card.handle_post(request)
            student.current_state = card.get_next_state()
            next_state_args = card.get_args()
            card = get_content(current_lesson, student.current_state, next_state_args)
            CardState.objects.get_or_create(student=student,
                                            lesson=current_lesson,
                                            state=student.current_state,
                                            card=card.to_json())
    except ObjectDoesNotExist:
        card = get_initial(current_lesson)
        CardState.objects.get_or_create(student=student,
                                        lesson=current_lesson,
                                        state=STATE_INITIAL,
                                        card=card.to_json())

    context["card"] = card.get_html(request)
    return render(request, 'lessons/lesson.html', context)
