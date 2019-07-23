from lesson.internet import states
from lesson.internet.aState import AState
from lesson.internet.bState import BState
from lesson.internet.cState import CState
from lesson.internet.initState import InitState
from lesson.lesson import Lesson
from lesson.lessonState import LessonState


class Internet(Lesson):
    _lessonStates = {
        states.INITSTATE: InitState,
        states.ASTATE: AState,
        states.BSTATE: BState,
        states.CSTATE: CState,
    }

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
    def get_state(s: int) -> LessonState:
        try:
            return Internet._lessonStates[s]()
        except KeyError:
            NotImplementedError("State does not exist: " + str(s))

    @staticmethod
    def get_all_states() -> [LessonState]:

        ls = []
        for s in Internet._lessonStates.values():
            ls.append(s())
        return ls
