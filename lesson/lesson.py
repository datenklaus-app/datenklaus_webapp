from lesson.lessonState import LessonState


class Lesson:
    @staticmethod
    def get_description():
        raise NotImplementedError()

    @staticmethod
    def get_short_description():
        raise NotImplementedError()

    @staticmethod
    def get_duration():
        raise NotImplementedError()

    @staticmethod
    def get_state(state) -> LessonState:
        """
        :return: A new Instance of the given state (s)
        """
        raise NotImplementedError()

    @staticmethod
    def get_all_states() -> [LessonState]:
        """
        :return: A list of all states (instantiated)
        """
        raise NotImplementedError()