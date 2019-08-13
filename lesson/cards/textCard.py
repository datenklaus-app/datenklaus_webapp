from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class TextCard(Card):
    def __init__(self, title, subtitle, text, state, template="lesson/cards/textCard.html"):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.state = state
        self.template = template

    def render(self, request, context):
        form = TextCardForm()
        context["title"] = self.title
        context["subtitle"] = self.subtitle
        context["text"] = self.text
        context["form"] = form
        context["state"] = self.state
        return render(request, self.template, context=context)

    def post(self, post):
        form = TextCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class TextCardForm(forms.Form):
    pass
