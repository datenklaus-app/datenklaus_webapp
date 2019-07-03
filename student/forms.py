from django import forms

from teacher.models import Room


class JoinRoomForm(forms.Form):
    username = forms.CharField(label="Nutzername", max_length=6)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), to_field_name='room_name', empty_label=None)
