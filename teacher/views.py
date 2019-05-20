from django.contrib.sessions.models import Session
from django.shortcuts import render

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
    data = {}
    for client in clients:
        data["name"] = client.user_name
        s = Session.objects.get(client.session)
        data["session"] = s.session_key
        data["last_activity"] = s.expire_date
    context = {'room_name': room_name, 'clients': data}
    return render(request, 'teacher/room.html', context=context)
