from lesson.lesson import Lesson
from lesson.lessonState import LessonState
from lesson.templateState import TemplateState


class Internet(Lesson):
    _lessonStates = {
        0: TemplateState("lesson/internet/0-intro.html", 0, 1,
                         "Einleitung", is_first=True),
        1: TemplateState("lesson/internet/1-Hinfuerung.html", 1, 2,
                         "Hinführung zum Thema"),
        2: TemplateState("lesson/internet/1-regel-1.html", 2, 3,
                         "1. Regel des Internets"),
        3: TemplateState("lesson/internet/2-internet-basics-1.html", 4, 5,
                         "Internet Basics 1 / INTERNET"),
        4: TemplateState("lesson/internet/2-regel-2.html", 4, 5,
                         "2. Regel des Internets"),
        5: TemplateState("lesson/internet/3-internet-basics-2.html", 5, 6,
                         "Internet-Basics 2 / Rechner, Laptop, Smartphone, Tablet"),
        6: TemplateState("lesson/internet/4-internet-basics-3.html", 6, 7,
                         "Internet-Basics 3 / WLAN oder Mobilfunk?"),
        7: TemplateState("lesson/internet/4-regel-3.html", 7, 8,
                         "3. Regel des Internets"),
        8: TemplateState("lesson/internet/5-internet-basics-4.html", 8, 9,
                         "Internet-Basics 4 / Zugriff auf Webseiten, Apps oder andere Dienstleistungen"),
        9: TemplateState("lesson/internet/6-hinfuerung-daten.html", 9, None, "Daten - 'Überleitung", is_final=True),
    }

    @staticmethod
    def title() -> str:
        return "Internet"

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
