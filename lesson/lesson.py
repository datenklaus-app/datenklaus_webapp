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
        raise NotImplementedError()
