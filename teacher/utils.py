import http
import json
from enum import Enum

from django.http import JsonResponse, HttpResponse

from lesson.lessonUtil import get_lesson, all_lessons
from student.models import Student
from teacher.models import Room


def get_room_and_lessons(room_name):
    room = Room.objects.get(room_name=room_name)
    prev_string = room.previous_lessons
    tmp = []
    prev_lessons = []
    if prev_string:
        tmp = json.loads(room.previous_lessons)
        prev_lessons = [{'name': l} for l in tmp]
    lessons = []
    for n, l in all_lessons().items():
        if n not in tmp and n != room.lesson:
            lessons.append({'name': n, 'description': l.description()})
    return room, lessons, prev_lessons


def get_students_for_room(room_name):
    try:
        room = Room.objects.get(room_name=room_name)
        lesson = get_lesson(room.lesson)
    except Room.DoesNotExist as e:
        raise e
    students = Student.objects.filter(room=room_name)
    student_info = []
    for student in students:
        lesson_state = lesson.state(student.current_state).name()
        student_info.append({"name": student.user_name,
                             "id": student.pk,
                             "progress": lesson_state,
                             "is_syncing": student.is_syncing,
                             "is_finished": student.is_finished})
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
