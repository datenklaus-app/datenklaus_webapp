class TeachingModule:
    @staticmethod
    def get_description():
        raise NotImplementedError()

    @staticmethod
    def get_short_descripton():
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

STATE_INITIAL = 0