from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student.models import Student
from teacher.constants import RoomStates
from teacher.models import Room
from .forms import JoinRoomForm


def index(request):
    return render(request, 'student/index.html')


def select_room(request):
    if request.is_ajax():
        rooms = Room.objects.all()
        room_names = []
        for r in rooms:
            if r.state is RoomStates.WAITING.value:
                room_names.append(r.room_name)
        return JsonResponse({'rooms': room_names})
    try:
        student = Student.objects.get(session=request.session.session_key)
        if student.room.state is not RoomStates.CLOSED.value:
            return HttpResponseRedirect(reverse('lesson'))
    except ObjectDoesNotExist:
        # NOTE: we need to manually set this to ensure that the user's session
        # is saved on the first request
        request.session.create()
        pass

    form = JoinRoomForm()
    context = {'form': form}
    return render(request, 'student/join_room.html', context)


def join_room(request):
    if request.method != "POST":
        return HttpResponseNotFound()

    form = JoinRoomForm(request.POST)

    # Note: Maybe add notification if form was invalid
    if not form.is_valid():
        return HttpResponseRedirect(reverse('student'))

    # Make sure we only have one existing student object per session
    for student in Student.objects.filter(session=request.session.session_key):
        student.delete()

    Student.objects.get_or_create(
        user_name=form.cleaned_data['username'],
        room=form.cleaned_data['room'],
        session=Session.objects.get(session_key=request.session.session_key),
        current_state=0,
    )

    return HttpResponseRedirect(reverse('lesson'))


def leave_room(request):
    for s in Student.objects.filter(session=request.session.session_key):
        s.delete()
    return HttpResponseRedirect(reverse("index"))
