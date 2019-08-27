from lesson.diceware.diceware import Diceware
from lesson.internet.internet import Internet
from lesson.lesson import Lesson
from student.models import Student

_lessons = {"Internet": Internet, "Diceware": Diceware}


def all_lessons() -> {str: Lesson}:
    """
    Returns all existing lessons as dictionary
    :return: Dictionary where:
             key: Name of Lesson
             value: Lesson
    """
    return _lessons


def get_lesson(name: str):
    """
    :param name: A string representing the lessons name
    :return: The Class representing the lesson given by name parameter
    """
    try:
        return _lessons[name]
    except KeyError as e:
        raise KeyError("Lesson does not exist: " + name) from e


def in_sync_state(lesson: str, state: int):
    return get_lesson(lesson).state(state).is_sync()


def in_final_state(lesson: str, state: int):
    return get_lesson(lesson).state(state).is_final()


def all_synced(room):
    for student in Student.objects.filter(room=room):
        if not in_sync_state(student.room.lesson, student.current_state):
            return False
    return True


def all_finished(room):
    for student in Student.objects.filter(room=room):
        if not in_final_state(student.room.lesson, student.current_state):
            return False
    return True
