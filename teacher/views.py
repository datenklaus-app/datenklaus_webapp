from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from lesson.views import get_lessons_list, get_lessons_description
from teacher import random_word_chain
from teacher.models import Room
from teacher.utils import get_students_for_room, ajax_bad_request, Cmd


def index(request):
    mod = get_lessons_list()
    for i in range(0, 10):
        mod.append(mod[0] + str(i))
    lessons = []
    # TODO exclude existing rooms from name suggestions
    for m in mod:
        lessons.append({'name': m, 'description': get_lessons_description(m)})
    context = {'random_room': random_word_chain.random_word_chain(), 'lessons': lessons}
    return render(request, 'teacher/index.html', context=context)


def room(request, room_name):
    if request.is_ajax():
        return HttpResponseBadRequest()
    if request.session.get("room") == "":
        request.session["room"] = room_name
    if request.method == "POST":
        lesson = request.POST.get("lesson", None)
        if lesson is None:
            return HttpResponseBadRequest()
        # TODO: Sanitizing and Error Handling
        #    if lesson is None or lesson not in get_lessons_list():
        #       return HttpResponseBadRequest('Invalid Lesson')
        # TODO: Password
        try:
            Room.objects.get(room_name=room_name)
            # TODO: better error message
            return HttpResponseBadRequest()
        except Room.DoesNotExist:
            Room.objects.create(room_name=room_name, lesson=lesson)
            return HttpResponseRedirect(reverse("room", args=[room_name]))
    try:
        r = Room.objects.get(room_name=room_name)
        context = {'room_name': room_name, 'lesson': r.lesson, 'state': r.state}
        return render(request, 'teacher/teacher_room.html', context=context)
    except Room.DoesNotExist:
        return HttpResponseRedirect(reverse("teacher_index"))


def get_rooms(request):
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


def refresh_student_list(request):
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
        return JsonResponse({'data': None})
    except Room.DoesNotExist:
        return ajax_bad_request(room_name)
