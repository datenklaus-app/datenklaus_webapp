from lesson.lessonState import LessonState


class Lesson:
    @staticmethod
    def description():
        raise NotImplementedError()

    @staticmethod
    def short_description():
        raise NotImplementedError()

    @staticmethod
    def duration():
        raise NotImplementedError()

    @staticmethod
    def state(state) -> LessonState:
        """
        :return: A new Instance of the given state (s)
        """
        raise NotImplementedError()

    @staticmethod
    def all_states() -> [LessonState]:
        """
        :return: A list of all states (instantiated)
        """
        raise NotImplementedError()