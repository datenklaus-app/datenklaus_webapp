from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render

from student.models import Student
from teacher import constants
from teacher.models import Room


def index(request):
    from teacher import random_word_chain
    context = {'random_room': random_word_chain.random_word_chain(), }
    return render(request, 'teacher/index.html', context=context)


def room(request, room_name):
    if request.session.get("room") == "":
        request.session["room"] = room_name
    created = Room.objects.get_or_create(room_name=room_name)[1]
    if created or not request.is_ajax():
        context = {'room_name': room_name}
        return render(request, 'teacher/teacher_room.html', context=context)
    clients = Student.objects.filter(room=room_name)
    clients_info = []
    for client in clients:
        s = Session.objects.get(session_key=client.session)
        decoded = s.get_decoded()
        module_state = decoded.get("module_state", constants.MODULE_STATE_WAITING)
        clients_info.append({"name": client.user_name,
                             "session": s.session_key,
                             "progress": module_state,
                             "expiry": s.expire_date})
    return JsonResponse({"clients": clients_info})
