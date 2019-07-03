from django.http import JsonResponse
from django.shortcuts import render

from lesson.views import get_lessons_list, get_lessons_description
from teacher.models import Room
from teacher.utils import get_students_for_room


def index(request):
    from teacher import random_word_chain
    context = {'random_room': random_word_chain.random_word_chain(), }
    return render(request, 'teacher/index.html', context=context)


def room(request, room_name):
    if request.session.get("room") == "":
        request.session["room"] = room_name
    buf = Room.objects.get_or_create(room_name=room_name)
    r = buf[0]
    created = buf[1]
    if created or not request.is_ajax():
        mod = get_lessons_list()
        modules = []
        for m in mod:
            modules.append({'name': m, 'description': get_lessons_description(m)})
        context = {'room_name': room_name, 'modules': modules}
        return render(request, 'teacher/teacher_room.html', context=context)
    rtype = request.POST.get('type', None)
    if rtype is None:
        raise ConnectionError
    if rtype == "students":
        students = get_students_for_room(room_name)
        return JsonResponse({"students": students})
    else:
        module = request.POST.get("module", None)
        if module is None or module not in get_lessons_list():
            return JsonResponse({"error": "module not found"})
        else:
            r.module = module
            r.save()
            return JsonResponse({"error": "none"})
