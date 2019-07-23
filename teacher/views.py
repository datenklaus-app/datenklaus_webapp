from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from lesson.lessonUtil import all_lessons
from teacher import random_word_chain
from teacher.models import Room
from teacher.utils import get_students_for_room, ajax_bad_request, Cmd, HttpResponseNoContent


def index(request):
    room_name = request.session.get("room", None)
    if room_name is not None:
        try:
            Room.objects.get(room_name=room_name)
            return HttpResponseRedirect(reverse("room", args={room_name}))
        except Room.DoesNotExist:
            del request.session["room"]
            request.session.save()
    lessons = [{'name': n, 'description': l.description()} for n, l in all_lessons().items()]
    rd = random_word_chain.random_word_chain()
    rooms = Room.objects.all()
    i = 0
    while rooms.filter(room_name=rd).exists():
        i += 1
        if i == 100:
            rd = ""
            break
        rd = random_word_chain.random_word_chain()
    context = {'random_room': rd, 'lessons': lessons}
    return render(request, 'teacher/index.html', context=context)


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
        password = request.POST.get("room_password", None)
        if password is None:
            return HttpResponseBadRequest()
        # TODO: Sanitizing and Error Handling
        #    if lesson is None or lesson not in get_lessons_list():
        #       return HttpResponseBadRequest('Invalid Lesson')
        # TODO: Password

        try:
            Room.objects.get(room_name=room_name)
            return ajax_bad_request("Room already exist: " + room_name)
        except Room.DoesNotExist:
            Room.objects.create(room_name=room_name, lesson=lesson, password=password)
            return HttpResponseNoContent()


def room(request, room_name):
    r = request.session.get("room", None)
    if r is None:
        request.session["room"] = room_name
    try:
        r = Room.objects.get(room_name=room_name)
        context = {'room_name': room_name, 'lesson': r.lesson, 'state': r.state}
        return render(request, 'teacher/teacher_room.html', context=context)
    except Room.DoesNotExist:
        return HttpResponseRedirect(reverse("teacher_index"))


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
    cmd = Cmd(int(b))
    # TODO: Validate and sanitize
    # TODO: Check permission
    try:
        r = Room.objects.get(room_name=room_name)
        r.state = cmd.value
        r.save()
        return HttpResponseNoContent()
    except Room.DoesNotExist:
        return ajax_bad_request("Room doesn't exist: " + room_name)
