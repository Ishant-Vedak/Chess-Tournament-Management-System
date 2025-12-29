from django import forms
from .models import Tournament

class CreateTournament(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ("name", "status", "type", "club")

    