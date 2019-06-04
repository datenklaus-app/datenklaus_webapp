from django.http import JsonResponse
from django.shortcuts import render

from lessons.views import get_all
from teacher.models import Room
from teacher.utils import get_students_for_room


def index(request):
    from teacher import random_word_chain
    context = {'random_room': random_word_chain.random_word_chain(), }
    return render(request, 'teacher/index.html', context=context)


def room(request, room_name):
    if request.session.get("room") == "":
        request.session["room"] = room_name
    created = Room.objects.get_or_create(room_name=room_name)[1]
    if created or not request.is_ajax():
        modules = get_all()
        context = {'room_name': room_name, 'modules': modules}
        return render(request, 'teacher/teacher_room.html', context=context)
    students = get_students_for_room(room_name)
    return JsonResponse({"students": students})
