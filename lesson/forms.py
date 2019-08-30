from django import forms


class TemplateCardForm(forms.Form):
    pass


class RangeSelectForm(forms.Form):
    value = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, choices, post=None):
        super(RangeSelectForm, self).__init__(post)
        self.fields["value"].choices = choices
