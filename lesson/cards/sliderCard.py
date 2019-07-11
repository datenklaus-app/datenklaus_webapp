from chartjs.views.lines import BaseLineChartView
from django import forms
from django.shortcuts import render
from django.template.loader import render_to_string

from lesson.cards.card import Card
from lesson.models import SliderCardModel


class SliderCard(Card):
    def __init__(self, title, min_val, max_val, state):
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.state = state

    def handle_post(self, post, student):
        form = self._make_form(post=post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()

        obj = SliderCardModel.objects.get_or_create(student=student, room=student.room, state=self.state)[0]
        obj.selected_value = form.cleaned_data['svalue']
        obj.save()

    def render(self, request, context):
        context["title"] = self.title
        context["form"] = self._make_form()
        context["min_value"] = str(self.min_val)
        context["max_value"] = str(self.max_val)
        context["state"] = self.state
        return render(request, 'lessons/cards/sliderCard.html', context=context)

    #FIXME: use form constructor!?
    def _make_form(self, post=None):
        if post is not None:
            form = self.SliderCardForm(post)
        else:
            form = self.SliderCardForm()
        form.declared_fields["svalue"].initial = (self.min_val + self.max_val) // 2
        form.declared_fields["svalue"].min_value = self.min_val
        form.declared_fields["svalue"].max_value = self.max_val
        return form

    class SliderCardForm(forms.Form):
        svalue = forms.IntegerField()
