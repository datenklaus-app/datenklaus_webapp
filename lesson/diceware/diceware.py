from lesson.lesson import Lesson
from lesson.states.lessonState import LessonState
from lesson.states.templateState import TemplateState


class Diceware(Lesson):
    _lessonStates = {
        0: TemplateState("lesson/diceware/0-intro.html", 0, 1,
                         "Modultitel", is_first=True),
        1: TemplateState("lesson/diceware/1-comic.html", 1, 2,
                         "Comic"),
        2: TemplateState("lesson/diceware/2-spielprinzip.html", 2, 3,
                         "Spielprinzip"),
        3: TemplateState("lesson/diceware/3-warum-diceware.html", 3, 4,
                         "Warum Diceware"),
        4: TemplateState("lesson/diceware/4-1-spiel-erklaerung.html", 4, 5,
                         "Anleitung Teil 1"),
        5: TemplateState("lesson/diceware/4-2-spiel-erklaerung.html", 5, 6,
                         "Anleitung Teil 2"),
        6: TemplateState("lesson/diceware/5-wuerfelspiel.html", 6, None,
                         "Würfelspiel",
                         is_final=True),
    }

    @staticmethod
    def title() -> str:
        return "Diceware"

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
