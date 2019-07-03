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
    def initial():
        raise NotImplementedError()

    @staticmethod
    def next(current_state, arguments):
        raise NotImplementedError()

