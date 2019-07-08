from lesson.internet.aState import AState
from lesson.internet.bState import BState
from lesson.internet.initState import InitState
from lesson.internet.states import BSTATE, ASTATE, INITSTATE
from lesson.lessonState import LessonState
from lesson.lesson import Lesson


class Internet(Lesson):
    STRING = "INTERNET"

    @staticmethod
    def get_description():
        pass

    @staticmethod
    def get_short_description():
        pass

    @staticmethod
    def get_duration():
        pass

    @staticmethod
    def get_state(state) -> LessonState:
        if state == INITSTATE:
            return InitState()
        elif state == ASTATE:
            return AState()
        elif state == BSTATE:
            return BState()
