class Card:
    def get_html(self, request):
        raise NotImplementedError("Error: Using Card Interface function")

    def handle_post(self, request, student, lesson, state):
        raise NotImplementedError("Error: Using Card Interface function")

    class InvalidCardFormError(Exception):
        pass
