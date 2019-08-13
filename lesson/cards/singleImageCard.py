from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class SingleImageCard(Card):
    def __init__(self, title, image, state, template='lesson/cards/singleImageCard.html'):
        self.title = title
        self.image = image
        self.state = state
        self.template = template

    def render(self, request, context):
        form = SingleImageCardForm()
        context["title"] = self.title
        context["img"] = self.image
        context["form"] = form
        context["state"] = self.state
        return render(request, self.template, context=context)

    def post(self, post):
        form = SingleImageCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class SingleImageCardForm(forms.Form):
    pass
