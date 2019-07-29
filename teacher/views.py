from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from lesson.lessonUtil import all_lessons
from student.models import Student
from teacher.constants import RoomStates
from teacher.models import Room
from teacher.random_word_chain import random_word
from teacher.utils import get_students_for_room, ajax_bad_request, Cmd, HttpResponseNoContent


def join(request):
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
            # return HttpResponseRedirect(reverse('teacher_index', {'room_name': room_name}))
            return HttpResponseNoContent()


def index(request):
    room_name = request.GET.get("room_name", None)
    lessons = [{'name': n, 'description': l.description()} for n, l in all_lessons().items()]
    context = {'lessons': lessons}
    if room_name is not None:
        try:
            room = Room.objects.get(room_name=room_name)
            context.update([('room_name', room_name), ('lesson', room.lesson), ('state', room.state)])
        except Room.DoesNotExist:
            pass
    return render(request, 'teacher/index.html', context=context)


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
