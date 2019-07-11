from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class DefaultCard(Card):
    def __init__(self, title, subtitle, text, state):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.state = state

    def render(self, request, context):
        form = DefaultCardForm()
        context["title"] = self.title
        context["subtitle"] = self.subtitle
        context["text"] = self.text
        context["form"] = form
        context["state"] = self.state
        return render(request, 'lessons/cards/defaultCard.html', context=context)

    def handle_post(self, post, student):
        form = DefaultCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class DefaultCardForm(forms.Form):
    pass
