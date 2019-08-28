from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class ImageCard(Card):
    def __init__(self, images=None, template='lesson/cards/imageCard.html', title=None):
        self.images = images
        self.template = template
        self.title = title

    def render(self, request, context):
        form = ImageCardForm()
        context["images"] = self.images
        context["form"] = form
        context["title"] = self.title
        return render(request, self.template, context=context)

    def post(self, post):
        form = ImageCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class ImageCardForm(forms.Form):
    pass
