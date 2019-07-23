from lesson.internet.internet import Internet
from lesson.lesson import Lesson


def all_lessons() -> {str: Lesson}:
    """
    Returns all existing lessons as dictionary
    :return: Dictionary where:
             key: Name of Lesson
             value: Lesson
    """
    return {"Internet": Internet}


def get_lesson(name: str):
    try:
        return all_lessons()[name]
    except KeyError:
        raise NotImplementedError("Lesson does not exist: " + name)
