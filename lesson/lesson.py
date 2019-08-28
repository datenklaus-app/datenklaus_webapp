from lesson.lessonState import LessonState


class Lesson:
    @staticmethod
    def title() -> str:
        """
        :return: A string containing a user readable title of the lesson
        """
        raise NotImplementedError()


    @staticmethod
    def description() -> str:
        """
        :return: A string containing a user readable description of the lesson
        """
        raise NotImplementedError()

    @staticmethod
    def short_description() -> str:
        """
        :return: A string containing a short user readable description of the lesson
        """
        raise NotImplementedError()

    @staticmethod
    def duration() -> int:
        """
        :return: The approximate duration of this lesson
        """
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
