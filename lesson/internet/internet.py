from lesson.internet import states
from lesson.internet.aState import AState
from lesson.internet.bState import BState
from lesson.internet.cState import CState
from lesson.internet.initState import InitState
from lesson.lessonState import LessonState
from lesson.lesson import Lesson


class Internet(Lesson):
    STRING = "INTERNET"

    @staticmethod
    def get_description():
        return "Eine Einführung in das Internet"

    @staticmethod
    def get_short_description():
        return "Eine Einführung in das Internet"

    @staticmethod
    def get_duration():
        return 45

    @staticmethod
    def get_state(state) -> LessonState:
        if state == states.INITSTATE:
            return InitState()
        elif state == states.ASTATE:
            return AState()
        elif state == states.BSTATE:
            return BState()
        elif state == states.CSTATE:
            return CState()
