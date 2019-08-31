from lesson.lesson import Lesson
from lesson.lessonState import LessonState
from lesson.templateState import TemplateState


class TooMuchTime(Lesson):
    _lessonStates = {
        0: TemplateState("lesson/toomuchtime/0-intro.html", 0, 1,
                         "Modultitel", is_first=True, is_final=True),
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
