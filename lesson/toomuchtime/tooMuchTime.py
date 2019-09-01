from lesson.lesson import Lesson
from lesson.states.lessonState import LessonState
from lesson.states.rangeSelectState import RangeSelectState
from lesson.states.templateState import TemplateState


class TooMuchTime(Lesson):
    _lessonStates = {
        0: TemplateState("lesson/toomuchtime/0-intro.html", 0, 1,
                         "Modultitel", is_first=True),
        1: TemplateState("lesson/toomuchtime/1-comic.html", 1, 2,
                         "Comic"),
        2: TemplateState("lesson/toomuchtime/2-info.html", 2, 3,
                         "Einleitung"),
        3: TemplateState("lesson/toomuchtime/3-hinfuerung.html", 3, 4,
                         "Hinfürung zum Fragebogen"),
        4: RangeSelectState("lesson/toomuchtime/4-7-fragen.html", 4, 5,
                            "Fragen(1)",
                            question="Wie häufig bist du online?",
                            choices=["mehrmals täglich",
                                     " einmal am Tag",
                                     "mehrmals die Woche",
                                     "einmal die Woche",
                                     "seltener / nie"]),

        5: RangeSelectState("lesson/toomuchtime/4-7-fragen.html", 5, 6,
                            "Fragen(2)",
                            question="Welches Gerät nutzt du meistens für einen Zugang zum Internet?",
                            choices=["Smartphone",
                                     "Tablet",
                                     "Laptop",
                                     "PC/Rechner",
                                     "Smartwatch",
                                     "Andere"]),

        6: RangeSelectState("lesson/toomuchtime/4-7-fragen.html", 6, 7,
                            "Fragen(3)",
                            question="Wieviel Zeit verbringst du pro Tag mit deinem internetfähigen Gerät?",
                            choices=["weniger als eine Stunde",
                                     "ein bis zwei Stunden",
                                     "zwei bis drei Stunden",
                                     "drei bis vier Stunden",
                                     "mehr als vier Stunden"]),
        7: RangeSelectState("lesson/toomuchtime/4-7-fragen.html", 7, 8,
                            "Fragen(4)",
                            question="Wofür nutzt du das Internet hauptsächlich?",
                            choices=["Zum Chatten mit der Familie und/oder Freund*innen",
                                     "Für Spiele (z.B. Game-Apps)",
                                     "Zur Unterhaltung (z.B. Videos/Youtube)",
                                     "Für Plattformnetzwerke wie z.B. Facebook oder Twitter",
                                     "Um Informationen und/oder Nachrichten zu erhalten"],
                            is_final=True),
    }

    @staticmethod
    def title() -> str:
        return "(Zu viel) Zeit im Internet verbringen "

    @staticmethod
    def description():
        return "Warum wir zu viel Zeit im Internet verbringen"

    @staticmethod
    def short_description():
        return "Warum wir zu viel Zeit im Internet verbringen"

    @staticmethod
    def duration():
        return 45

    @staticmethod
    def state(s: int) -> LessonState:
        try:
            return TooMuchTime._lessonStates[s]
        except KeyError:
            NotImplementedError("State does not exist: " + str(s))

    @staticmethod
    def all_states() -> [LessonState]:

        ls = []
        for s in TooMuchTime._lessonStates.values():
            ls.append(s)
        return ls
