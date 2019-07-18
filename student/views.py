from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student.models import Student
from teacher.models import Room
from .forms import JoinRoomForm


def index(request):
    if request.is_ajax():
        rooms = Room.objects.all()
        room_names = []
        for r in rooms:
            room_names.append(r.room_name)
        return JsonResponse({'rooms': room_names})

    try:
        student = Student.objects.get(session=request.session.session_key)
        if student.room.lesson is not None:
            context = {'sname': student.user_name, 'rname': student.room}
            return render(request, 'student/room_waiting.html', context)
    except ObjectDoesNotExist:
        # NOTE: we need to manually set this to ensure that the user's session
        # is saved on the first request
        request.session.create()
        pass

    form = JoinRoomForm()
    context = {'form': form}
    return render(request, 'student/index.html', context)


def join_room(request):
    if request.is_ajax():
        student = Student.objects.get(session=request.session.session_key)
        if student.room.lesson is None:
            return HttpResponseNotFound("Student has not joined a room yet")
        else:
            return JsonResponse({'lesson_started': True})

    form = JoinRoomForm(request.POST)
    if not form.is_valid():
        raise KeyError()  # FIXME

    # Make sure we only have one existing student object per session
    for student in Student.objects.filter(session=request.session.session_key):
        student.delete()

    Student.objects.get_or_create(
        user_name=form.cleaned_data['username'],
        room=form.cleaned_data['room'],
        session=Session.objects.get(session_key=request.session.session_key),
        current_state=0,
    )

    context = {'sname': form.cleaned_data['username'], 'rname': form.cleaned_data['room']}
    return render(request, 'student/room_waiting.html', context)


def leave_room(request):
    for s in Student.objects.filter(session=request.session.session_key):
        s.delete()
    return HttpResponseRedirect(reverse("index"))
