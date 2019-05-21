from django.contrib.sessions.models import Session
from django.shortcuts import render

from teacher import constants
from teacher.models import Client, Room


def index(request):
    from teacher import random_word_chain
    context = {'random_room': random_word_chain.random_word_chain(), }
    return render(request, 'teacher/index.html', context=context)


def room(request, room_name):
    if request.session.get("room") == "":
        request.session["room"] = room_name
    created = Room.objects.get_or_create(room_name=room_name)[1]
    clients = {} if created else Client.objects.filter(room=room_name)
    clients_info = []
    for client in clients:
        s = Session.objects.get(session_key=client.session)
        decoded = s.get_decoded()
        module_state = decoded.get("module_state", constants.MODULE_STATE_WAITING)
        clients_info.append(
            (client.user_name, s.session_key, module_state, s.expire_date))
    context = {'room_name': room_name,
               'clients_info': clients_info}
    return render(request, 'teacher/teacher_room.html', context=context)
