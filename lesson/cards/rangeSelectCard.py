from django import forms
from django.shortcuts import render

from lesson.cards.card import Card


class RangeSelectCard(Card):
    def __init__(self, title, choices, state):
        self.title = title
        self.choices = choices
        self.state = state

    def handle_post(self, post):
        form = RangeSelectForm(self.choices, post=post)
        if not form.is_valid():
            raise Card.InvalidCardFormError(form.errors)
        return form.cleaned_data

    def render(self, request, context):
        context["title"] = self.title
        context["form"] = RangeSelectForm(self.choices)
        context["state"] = self.state
        return render(request, 'lessons/cards/rangeSelectCard.html', context=context)


class RangeSelectForm(forms.Form):
    value = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, choices, post=None):
        super(RangeSelectForm, self).__init__(post)
        self.fields["value"].choices = choices
