from lesson.diceware.diceware import Diceware
from lesson.internet.internet import Internet
from lesson.lesson import Lesson


def all_lessons() -> {str: Lesson}:
    """
    Returns all existing lessons as dictionary
    :return: Dictionary where:
             key: Name of Lesson
             value: Lesson
    """
    return {"Internet": Internet, "Diceware": Diceware}


def get_lesson(name: str):
    try:
        return all_lessons()[name]
    except KeyError:
        raise NotImplementedError("Lesson does not exist: " + name)
