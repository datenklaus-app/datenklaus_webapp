from django import forms
from django.template.loader import render_to_string

from lesson.cards.card import Card


class DefaultCard(Card):
    def __init__(self, title, subtitle, text, state):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.state = state

    def get_html(self, request):
        form = DefaultCardForm()
        context = {"title": self.title,
                   "subtitle": self.subtitle,
                   "text": self.text,
                   "form": form,
                   "state": self.state}
        return render_to_string('lessons/cards/defaultCard.html', request=request, context=context)

    def handle_post(self, post, student, lesson):
        form = DefaultCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class DefaultCardForm(forms.Form):
    pass