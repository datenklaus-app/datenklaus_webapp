import json
from django.template.loader import render_to_string

from lesson.lessons.card import Card


class DefaultCard(Card):
    @staticmethod
    def from_json(arglist):
        return DefaultCard(arglist[0], arglist[1], arglist[2], arglist[3])
        pass

    def __init__(self, title, subtitle, text, next_state):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.next_state = next_state

    def get_html(self, request):
        context = {"title": self.title,
                   "subtitle": self.subtitle,
                   "text": self.text,
                   "next_state": self.next_state,
                   "request": request}

        return render_to_string('lessons/default.html', context)

    def handle_args(self, args):
        pass

    def handle_post(self, request):
        return

    def get_next_state(self):
        return self.next_state

    def get_args(self):
        return None

    def to_json(self):
        return json.dumps([self.__class__.__name__,
                           self.title,
                           self.subtitle,
                           self.text,
                           self.next_state])
