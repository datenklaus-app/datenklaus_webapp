from django.shortcuts import render


def index(request):
    from teaching_module import random_word_chain
    context = {'random_room': random_word_chain.random_word_chain(), }
    return render(request, 'teaching_module/index.html', context=context)


def room(request, room_name):
    context = {'room_name': room_name}
    return render(request, 'teaching_module/room.html', context=context)
