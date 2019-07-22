class Card:
    def render(self, request):
        raise NotImplementedError("Error: Using Card Interface function")

    def handle_post(self, post):
        raise NotImplementedError("Error: Using Card Interface function")

    class InvalidCardFormError(Exception):
        pass
