from lesson.lesson import Lesson
from lesson.lessonState import LessonState
from lesson.templateState import TemplateState


class Internet(Lesson):
    _lessonStates = {
        0: TemplateState("lesson/internet/initState.html", 0, 1,
                         "Einleitung"),
        1: TemplateState("lesson/internet/a-textCard.html", 1, 2,
                         "Hinführung zum Thema"),
        2: TemplateState("lesson/internet/b-textCard.html", 2, 3,
                         "Internet Basics 1 / INTERNET"),
        3: TemplateState("lesson/internet/c-textCard.html", 3, 4,
                         "Internet-Basics 2 / Rechner, Laptop, Smartphone, Tablet", is_sync=True),
        4: TemplateState("lesson/internet/d-textCard.html", 4, 5,
                         "Internet-Basics 3 / WLAN oder Mobilfunk?"),
        5: TemplateState("lesson/internet/e-textCard.html", 5, 6,
                         "Internet-Basics 4 / Zugriff auf Webseiten, Apps oder andere Dienstleistungen"),
        6: TemplateState("lesson/internet/f-textCard.html", 6, None,
                         "Daten - Hinführung"),
    }

    @staticmethod
    def description():
        return "Eine Einführung in das Internet"

    @staticmethod
    def short_description():
        return "Eine Einführung in das Internet"

    @staticmethod
    def duration():
        return 45

    @staticmethod
    def state(s: int) -> LessonState:
        try:
            return Internet._lessonStates[s]
        except KeyError:
            NotImplementedError("State does not exist: " + str(s))

    @staticmethod
    def all_states() -> [LessonState]:

        ls = []
        for s in Internet._lessonStates.values():
            ls.append(s)
        return ls
