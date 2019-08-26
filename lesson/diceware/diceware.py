from lesson.diceware import states
from lesson.diceware.aState import AState
from lesson.diceware.bState import BState
from lesson.diceware.cState import CState
from lesson.diceware.dState import DState
from lesson.diceware.eState import EState
from lesson.diceware.initState import InitState
from lesson.lesson import Lesson
from lesson.lessonState import LessonState


class Diceware(Lesson):
    _lessonStates = {
        states.INITSTATE: InitState(),
        states.ASTATE: AState(),
        states.BSTATE: BState(),
        states.CSTATE: CState(),
        states.DSTATE: DState(),
        states.ESTATE: EState(),
    }

    @staticmethod
    def description():
        return "Diceware"

    @staticmethod
    def short_description():
        return "Diceware short"

    @staticmethod
    def duration():
        return 45

    @staticmethod
    def state(s: int) -> LessonState:
        try:
            return Diceware._lessonStates[s]
        except KeyError:
            NotImplementedError("State does not exist: " + str(s))

    @staticmethod
    def all_states() -> [LessonState]:

        ls = []
        for s in Diceware._lessonStates.values():
            ls.append(s)
        return ls
