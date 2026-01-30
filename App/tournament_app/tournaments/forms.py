from django import forms
from .models import Tournament

class CreateTournament(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ("name", "status", "type", "club")

    
class TournamentSettings(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'creation_date', 'status', 'type', 'format', 'club'] 