from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from lesson.lessonUtil import get_lesson, all_lessons
from lesson.models import LessonSateModel
from student.models import Student
from teacher.constants import RoomStates
from teacher.models import Room
from teacher.random_word_chain import random_word
from teacher.utils import get_students_for_room, ajax_bad_request, Cmd, HttpResponseNoContent


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
        room = Room.objects.get(room_name=room_name)
        context = {'room_name': room_name, 'lesson': room.lesson, 'state': room.state}
        return render(request, 'teacher/overview.html', context=context)
    except Room.DoesNotExist:
        # TODO: Handle room deletion?
        return HttpResponseRedirect(reverse("teacher_index"))


def create(request):
    lessons = [{'name': n, 'description': l.description()} for n, l in all_lessons().items()]
    context = {'lessons': lessons}
    return render(request, 'teacher/create_room.html', context=context)


def create_room(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if request.method == "POST":
        room_name = request.POST.get("room_name", None)
        if room_name is None:
            return HttpResponseBadRequest()
        lesson = request.POST.get("lesson", None)
        if lesson is None:
            return HttpResponseBadRequest()
        # TODO: Sanitizing and Error Handling
        #    if lesson is None or lesson not in get_lessons_list():
        #       return HttpResponseBadRequest('Invalid Lesson')
        # TODO: Password
        try:
            Room.objects.get(room_name=room_name)
            return ajax_bad_request("Room already exist: " + room_name)
        except Room.DoesNotExist:
            Room.objects.create(room_name=room_name, lesson=lesson)
            return reverse("overview", args=room_name)


def results(request, room_name):
    try:
        room = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return ajax_bad_request("Room doesn't exist")
    no_students = Student.objects.filter(room=room).count()
    states = get_lesson(room.lesson).all_states()
    results = []
    for state in states:
        r = state.result_svg(room_name)
        if r is not None:
            completed = LessonSateModel.objects.filter(room=room, state=state.state_number()).count()
            results.append({'state_name': state.name(), 'completed': completed, 'svg': r})
    return JsonResponse({'results': results, 'no_students': no_students})


def leave_room(request):
    del request.session["room"]
    request.session.save()
    return HttpResponseRedirect(reverse("teacher_index"))


def rooms(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    rooms = [n['room_name'] for n in Room.objects.all().values('room_name')]
    return JsonResponse({'rooms': rooms})


def validate_room_name(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    # TODO: Validate and sanitize
    data = {'exists': Room.objects.filter(room_name=room_name).exists()}
    return JsonResponse(data)


def students(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    room_name = request.GET.get("room_name", None)
    # TODO: Validate and sanitize
    try:
        r = Room.objects.get(room_name=room_name)
        students = get_students_for_room(r)
        return JsonResponse({"students": students})
    except Room.DoesNotExist:
        return ajax_bad_request("Room " + room_name + " not found")


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
    elif cmd == Cmd.STOP:
        r.state = RoomStates.CLOSED.value
    elif cmd == Cmd.PAUSE:
        r.state = RoomStates.PAUSED.value
    else:
        return ajax_bad_request("Room command does not exist: " + str(cmd))

    r.save()
    return HttpResponseNoContent()


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
        Student(user_name=random_word(), session=None, room=room).save()
    return HttpResponseNoContent()
