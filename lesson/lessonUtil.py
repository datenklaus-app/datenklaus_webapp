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


def all_synced(room):
    for student in Student.objects.filter(room=room):
        if not student.is_syncing:
            return False
    return True


def all_finished(room):
    for student in Student.objects.filter(room=room):
        if not student.is_finished:
            return False
    return True
