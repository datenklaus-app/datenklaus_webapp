from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class ImageCard(Card):
    def __init__(self, images, state):
        self.images = images
        self.state = state

    def render(self, request, context):
        form = ImageCardForm()
        context["images"] = self.images
        context["form"] = form
        context["state"] = self.state
        return render(request, 'lesson/cards/imageCard.html', context=context)

    def handle_post(self, post):
        form = ImageCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class ImageCardForm(forms.Form):
    pass
