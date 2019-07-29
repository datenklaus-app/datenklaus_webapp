# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render

from lesson.lessonState import LessonState
from lesson.lessonUtil import get_lesson
from student.models import Student
from teacher.constants import RoomStates


def room_status(request):
    if not request.is_ajax():
        return HttpResponseNotFound()

    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return JsonResponse({"running": False, "redirect": "/"})

    if student.room.state == RoomStates.CLOSED.value:
        return JsonResponse({"running": False, "redirect": "/"})

    return JsonResponse({"running": student.room.state == RoomStates.RUNNING.value, "redirect": None})


def lesson(request, state_num=None):
    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/")

    room_state = RoomStates(student.room.state)

    if room_state == RoomStates.PAUSED:
        return render(request, "lesson/room/room_pause.html")
    elif room_state == RoomStates.WAITING:
        return render(request, "lesson/room/room_waiting.html",
                      context={"sname": student.user_name, "rname": student.room.room_name})
    elif room_state == RoomStates.CLOSED:
        return HttpResponseRedirect("/")

    if state_num is not None:
        student.current_state = state_num
    current_lesson = get_lesson(student.room.lesson)

    try:
        state = current_lesson.state(student.current_state)
        if request.method == 'POST':
            # FIXME : clean up this mess!
            state.post(request.POST, student)
            student.current_state = state.next_state(student)
            state = current_lesson.state(student.current_state)
            state.set_previous_state(student, state_num)
            student.save()
        else:  # FIXME: Handle potential error cases?
            student.save()  # Resend current card  if we receive a GET request

    except LessonState.LessonStateError as e:
        student.current_state = e.fallback_state
        state = current_lesson.state(e.fallback_state)

    context = {"lname": student.room.lesson, "rname": student.room, "previous_state": state.previous_state(student)}
    return state.render(request, student, context)
