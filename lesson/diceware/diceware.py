from lesson.lesson import Lesson
from lesson.lessonState import LessonState
from lesson.templateState import TemplateState


class Diceware(Lesson):
    _lessonStates = {
        0: TemplateState("lesson/diceware/init-imageCard.html", 0, 1,
                         "Einleitung", is_first=True),
        1: TemplateState("lesson/diceware/a-textCard.html", 1, 2,
                         "Hinführung zum Spiel"),
        2: TemplateState("lesson/diceware/b-textCard.html", 2, 3,
                         "Erklärung: Spielprinzip"),
        3: TemplateState("lesson/diceware/c-textCard.html", 3, 4,
                         "Erklärung: Spielt"),
        4: TemplateState("lesson/diceware/d-diceGameCard.html", 4, 5,
                         "Würfelspiel", is_sync=True),
        5: TemplateState("lesson/diceware/e-textCard.html", 5, 6,
                         "Abschluss",
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
