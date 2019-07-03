from lesson.lessons.defaultCard import DefaultCard
from .lesson import Lesson


class Internet(Lesson):
    @staticmethod
    def next(current_state, arguments):
        pass

    QUESTION_CURRENT_KNOWLEDGE = 1

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
    def initial():
        return DefaultCard("Willkommen",
                           "Heute lernen wir etwas über das Internet",
                           "Das Internet ist sehr toll",
                           Internet.QUESTION_CURRENT_KNOWLEDGE)
