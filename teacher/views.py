from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from lesson.views import get_lessons_list, get_lessons_description
from teacher import random_word_chain
from teacher.models import Room
from teacher.utils import get_students_for_room


def index(request):
    mod = get_lessons_list()
    for i in range(0, 10):
        mod.append(mod[0] + str(i))
    modules = []
    # TODO exclude existing rooms from name suggestions
    # TODO fill list of existing rooms
    for m in mod:
        modules.append({'name': m, 'description': get_lessons_description(m)})
    context = {'random_room': random_word_chain.random_word_chain(), 'modules': modules}
    return render(request, 'teacher/index.html', context=context)


def room(request, room_name):
    if request.session.get("room") == "":
        request.session["room"] = room_name
    if request.is_ajax():
        return refresh_student_list(room_name)
    if request.method == "POST":
        lesson = request.POST.get("lesson", None)
        # TODO: Error Handling
        #    if lesson is None or lesson not in get_lessons_list():
        #       return HttpResponseBadRequest('Invalid Lesson')
        buf = Room.objects.get_or_create(room_name=room_name)
        if buf[1]:
            buf[0].room_name = lesson
            buf[0].save()
        return HttpResponseRedirect(reverse("room", args=[room_name]))
    buf = Room.objects.get_or_create(room_name=room_name)
    r = buf[0]
    context = {'room_name': room_name, 'module': r.module}
    return render(request, 'teacher/teacher_room.html', context=context)


def refresh_student_list(room_name):
    r = Room.objects.get_or_create(room_name=room_name)[0]
    students = get_students_for_room(r)
    return JsonResponse({"students": students})
