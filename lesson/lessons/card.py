class Card:
    def get_html(self):
        raise NotImplementedError("Error: Using Card Interface function")

    def handle_post(self, request):
        raise NotImplementedError("Error: Using Card Interface function")

    def handle_args(self, args):
        raise NotImplementedError("Error: Using Card Interface function")

    def get_next_state(self):
        raise NotImplementedError("Error: Using Card Interface function")

    def get_args(self):
        raise NotImplementedError("Error: Using Card Interface function")

    def to_json(self):
        raise NotImplementedError("Error: Using Card Interface function")
