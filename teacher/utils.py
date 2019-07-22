import http
from enum import Enum

from django.contrib.sessions.models import Session
from django.http import JsonResponse, HttpResponse

from lesson.lessonUtil import get_lesson
from student.models import Student
from teacher.constants import LESSON_STATE_WAITING
from teacher.models import Room


def get_students_for_room(room_name):
    try:
        room = Room.objects.get(room_name=room_name)
        lesson = get_lesson(room.lesson)
    except Room.DoesNotExist as e:
        raise e
    students = Student.objects.filter(room=room_name)
    student_info = []
    for student in students:
        s = Session.objects.get(session_key=student.session)
        lesson_state = LESSON_STATE_WAITING if room.state == -1 else lesson.get_state(student.current_state).get_name()
        student_info.append({"name": student.user_name,
                             "session": s.session_key,
                             "progress": lesson_state,
                             "expiry": s.expire_date})
    return student_info


def ajax_bad_request(error_msg):
    response = JsonResponse({'err': error_msg})
    response.status_code = http.HTTPStatus.BAD_REQUEST
    return response


class HttpResponseNoContent(HttpResponse):
    status_code = 204


class Cmd(Enum):
    START = 0
    PAUSE = 1
    STOP = 2
