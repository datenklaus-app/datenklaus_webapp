import json
import re

from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from lesson.lessonUtil import get_lesson, all_lessons, all_synced, all_finished
from lesson.models import LessonStateModel
from student.models import Student
from teacher.constants import RoomStates
from teacher.models import Room
from teacher.random_word_chain import random_word
from teacher.utils import get_students_for_room, ajax_bad_request, Cmd, HttpResponseNoContent, get_room_and_lessons, \
    get_previous_lessons


# Regular requests

def index(request):
    try:
        room = request.session["room"]
    except KeyError:
        return render(request, 'teacher/index.html')

    return HttpResponseRedirect(reverse("overview", args=[room]))


def overview(request, room_name=None):
    if room_name is None:
        try:
            room_name = request.session["room"]
        except KeyError:
            return HttpResponseRedirect(reverse("teacher_index"))
    else:
        request.session["room"] = room_name

    try:
        room, lessons, _ = get_room_and_lessons(room_name)
        context = {'room_name': room_name, 'lessons': lessons, 'lesson': room.lesson, 'state': room.state,
                   "is_overview": True}
        return render(request, 'teacher/overview.html', context=context)
    except Room.DoesNotExist:
        del request.session["room"]
        return HttpResponseRedirect(reverse("teacher_index"))


def create(request):
    lessons = [{'name': n, 'description': l.description()} for n, l in all_lessons().items()]
    context = {'lessons': lessons}
    return render(request, 'teacher/create_room.html', context=context)


def results(request, room_name):
    try:
        room, lessons, prev_lessons = get_room_and_lessons(room_name)
    except Room.DoesNotExist:
        del request.session["room"]
        return HttpResponseRedirect(reverse("teacher_index"))

    context = {'room_name': room_name, 'lessons': lessons, 'lesson': room.lesson, 'prev_lessons': prev_lessons,
               'state': room.state,
               "is_results": True}
    return render(request, "teacher/results.html", context)


# Ajax requests

def create_room(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if request.method == "POST":
        room_name = request.POST.get("room_name", None)
        room_name = room_name.strip()
        if room_name is None:
            return ajax_bad_request("Error: empty room name")
        if re.search("[^A-Za-z0-9.-]", room_name):
            return ajax_bad_request("Error: room name contains unallowed characters")
        lesson = request.POST.get("lesson", None)
        if lesson is None:
            return ajax_bad_request("Error: no lesson set")
        try:
            get_lesson(lesson)
        except KeyError:
            return ajax_bad_request("Error: unknown lesson")
        try:
            Room.objects.get(room_name=room_name)
            return ajax_bad_request("Error: room already exist: " + room_name)
        except Room.DoesNotExist:
            Room.objects.create(room_name=room_name, lesson=lesson)
            return HttpResponseNoContent()


def get_results(request, room_name):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    try:
        room = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return ajax_bad_request("Room doesn't exist")
    lesson = request.GET.get("lesson", None)
    try:
        get_lesson(lesson)
    except KeyError:
        return ajax_bad_request("Error: unknown lesson")
    num_students = Student.objects.filter(room=room).count()
    states = get_lesson(lesson).all_states()
    state_results = []
    for state in states:
        r = state.result_svg(room_name)
        if r is not None:
            completed = LessonStateModel.objects.filter(room=room, state=state.state_number()).count()
            state_results.append({'state_name': state.name(), 'completed': completed, 'svg': r})
    return JsonResponse({'results': state_results, 'no_students': num_students, 'current_lesson': room.lesson,
                         'prev_lessons': get_previous_lessons(room)})


def get_rooms(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    rooms = [n['room_name'] for n in Room.objects.all().values('room_name')]
    return JsonResponse({'rooms': rooms})


def validate_room_name(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    data = {'exists': Room.objects.filter(room_name=room_name).exists()}
    return JsonResponse(data)


def remove_student(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    # TODO: Check auth / permission
    room_name = request.GET.get("room_name", None)
    try:
        r = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return ajax_bad_request("Room " + room_name + " not found")
    student = request.GET.get("student", None)
    if not student:
        return ajax_bad_request("Error: no such student")
    try:
        s = Student.objects.get(pk=student, room=r)
        s.delete()
    except Student.DoesNotExist:
        return ajax_bad_request("Error: student not in room")
    for l in LessonStateModel.objects.filter(room=r, student=s):
        l.delete()
    if Student.objects.filter(room=r).count() == 0:
        r.state = RoomStates.WAITING.value
        r.save()
    return JsonResponse({'state': r.state})


def remove_room(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    try:
        r = Room.objects.get(room_name=room_name)
        r.delete()
        return HttpResponseNoContent()
    except Room.DoesNotExist:
        return ajax_bad_request("Room " + room_name + " not found")


def get_students(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    try:
        students = get_students_for_room(room_name)
        return JsonResponse({"students": students})
    except Room.DoesNotExist:
        return ajax_bad_request("Room " + room_name + " not found")


def get_sync_state(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    try:
        r = Room.objects.get(room_name=room_name)
        synced = all_synced(room_name)
        finished = all_finished(room_name)
        return JsonResponse({"state": r.state, "finished": finished, "synced": synced})
    except Room.DoesNotExist:
        return ajax_bad_request("Room " + room_name + " not found")


def change_lesson(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    try:
        r = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return ajax_bad_request("Room " + room_name + " not found")
    lesson = request.GET.get("lesson", None)
    if lesson is None:
        return ajax_bad_request("Error: no lesson set")
    try:
        get_lesson(lesson)
    except KeyError:
        return ajax_bad_request("Error: unknown lesson")
    prev_lessons = get_previous_lessons(r)
    prev_lessons.append(r.lesson)
    r.previous_lessons = json.dumps(prev_lessons)
    r.lesson = lesson
    r.state = RoomStates.WAITING.value
    r.save()
    students = Student.objects.filter(room=r)
    for student in students:
        student.current_state = 0
        student.is_finished = False
        student.is_syncing = False
        student.save()
    return HttpResponseNoContent()


def control_cmd(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    b = request.GET.get("cmd", None)

    if b is None:
        return ajax_bad_request("Command not found")
    try:
        r = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return ajax_bad_request("Room doesn't exist: " + room_name)

    cmd = Cmd(int(b))
    if cmd == Cmd.START:
        r.state = RoomStates.RUNNING.value
        for student in Student.objects.filter(room=r):
            student.is_syncing = False
            student.is_finished = False
            student.save()
    elif cmd == Cmd.STOP:
        r.state = RoomStates.CLOSED.value
        for student in Student.objects.filter(room=r):
            student.delete()
    elif cmd == Cmd.PAUSE:
        r.state = RoomStates.PAUSED.value
    else:
        return ajax_bad_request("Room command does not exist: " + str(cmd))

    r.save()
    return HttpResponseNoContent()


# Debugging Only
def create_test_students(request):
    if not request.is_ajax():
        return HttpResponseBadRequest
    room_name = request.GET.get("room_name", None)
    if room_name is None:
        return HttpResponseBadRequest
    try:
        room = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return ajax_bad_request("Room" + room_name + " doesn't exist")
    for _ in range(0, 10):
        Student(user_name=random_word()[:6], session=None, room=room).save()
    return HttpResponseNoContent()
