# Create your views here.
import markdown
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from lesson.lessonState import LessonState
from lesson.lessonUtil import get_lesson
from lexicon import lexiconUtils
from student.models import Student
from teacher.constants import RoomStates


def room_status(request):
    if not request.is_ajax():
        return HttpResponseNotFound()

    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return JsonResponse({"running": False, "redirect": "/" })

    if student.room.state == RoomStates.CLOSED.value:
        return JsonResponse({"running": False, "redirect": "/", "syncing": student.is_syncing, })

    return JsonResponse({"running": student.room.state == RoomStates.RUNNING.value,
                         "syncing": student.is_syncing or student.is_finished,
                         "redirect": None})


def lesson(request):
    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    room_state = RoomStates(student.room.state)
    if room_state == RoomStates.PAUSED:
        return render(request, "lesson/pause.html")
    elif room_state == RoomStates.WAITING:
        return render(request, "lesson/waiting.html",
                      context={"sname": student.user_name, "rname": student.room.room_name})
    elif room_state == RoomStates.CLOSED:
        return HttpResponseRedirect(reverse("index"))

    current_lesson = get_lesson(student.room.lesson)

    if student.is_finished:
        entry = lexiconUtils.get_random_entry()
        context = {"lesson_title": current_lesson.title(),
                   "entry": entry.as_html()}
        return render(request, "lesson/finished.html", context=context)

    if student.is_syncing:
        entry = lexiconUtils.get_random_entry()
        context = {"entry": entry.as_html()}
        return render(request, "lesson/sync.html", context=context)

    current_state = current_lesson.state(student.current_state)

    context = {"lname": student.room.lesson,
               "rname": student.room,
               "is_first": current_state.is_first()}

    return current_state.render(request, student, context)


def lesson_previous(request):
    # Must NOT a post request
    if request.method == 'POST':
        return HttpResponseNotFound()

    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    current_lesson = get_lesson(student.room.lesson)
    current_state = current_lesson.state(student.current_state)

    prev_state = current_state.previous_state(student)
    if prev_state is not None:
        student.current_state = prev_state
        student.save()
    return HttpResponseRedirect(reverse("lesson"))


def lesson_next(request):
    # Must be a post request
    if not request.method == 'POST':
        return HttpResponseNotFound()

    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    current_lesson = get_lesson(student.room.lesson)
    current_state = current_lesson.state(student.current_state)

    if current_state.is_final():
        student.is_finished = True
        student.save()
        return HttpResponseRedirect(reverse("lesson"))

    # Handle post received from current state
    try:
        current_state.post(request.POST, student)
    except LessonState.LessonStateError as e:
        if e.fallback_state is None:
            return HttpResponseNotFound()
        student.current_state = e.fallback_state
        return HttpResponseRedirect(reverse("lesson"))

    # Transition to next state
    student.current_state = current_state.next_state(student)
    next_state = current_lesson.state(student.current_state)
    # Check if next state is sync state
    if next_state.is_sync():
        student.is_syncing = True
    else:
        next_state.set_previous_state(student, current_state.state_number())

    student.save()
    return HttpResponseRedirect(reverse("lesson"))
