from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class ImageCard(Card):
    def __init__(self, images, state, template='lesson/cards/imageCard.html'):
        self.images = images
        self.state = state
        self.template = template

    def render(self, request, context):
        form = ImageCardForm()
        context["images"] = self.images
        context["form"] = form
        context["state"] = self.state
        return render(request, self.template, context=context)

    def post(self, post):
        form = ImageCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class ImageCardForm(forms.Form):
    pass
