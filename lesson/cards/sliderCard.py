from django import forms
from django.template.loader import render_to_string

from lesson.cards.card import Card
from lesson.models import SliderCardModel


class SliderCard(Card):
    def __init__(self, title, min_val, max_val, state):
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.state = state

    def handle_post(self, post, student, lesson):
        form = self._make_form(post=post)
        if not form.is_valid():
            raise Card.InvalidCardFormError()

        obj = SliderCardModel.objects.get_or_create(student=student, lesson=lesson, state=self.state)[0]
        obj.selected_value = form.cleaned_data['svalue']
        obj.save()

    def get_html(self, request):
        context = {"title": self.title,
                   "form": self._make_form(),
                   "min_value": str(self.min_val),
                   "max_value": str(self.max_val),
                   "state": self.state}

        return render_to_string('lessons/cards/sliderCard.html', request=request, context=context)

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
