from django.contrib.sessions.models import Session

from student.models import Student
from teacher.constants import MODULE_STATE_WAITING


def get_students_for_room(room_name):
    students = Student.objects.filter(room=room_name)
    student_info = []
    for student in students:
        s = Session.objects.get(session_key=student.session)
        decoded = s.get_decoded()
        module_state = decoded.get("module_state", MODULE_STATE_WAITING)
        student_info.append({"name": student.user_name,
                             "session": s.session_key,
                             "progress": module_state,
                             "expiry": s.expire_date})
    return student_info
