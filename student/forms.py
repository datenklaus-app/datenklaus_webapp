from django import forms

from teacher.constants import RoomStates
from teacher.models import Room


class JoinRoomForm(forms.Form):
    username = forms.CharField(label="Nutzername", max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    room = forms.ModelChoiceField(queryset=Room.objects.filter(state=RoomStates.WAITING.value), to_field_name='room_name', empty_label=None)
