from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class TemplateCard(Card):
    def __init__(self, template):
        self.template = template

    def render(self, request, context):
        form = TemplateCardForm()
        context["form"] = form
        return render(request, self.template, context=context)

    def post(self, post):
        form = TemplateCardForm(post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()


class TemplateCardForm(forms.Form):
    pass
