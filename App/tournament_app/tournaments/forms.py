from django import forms
from .models import Tournament, Participant

class CreateTournament(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ("name", "status", "type", "club")

    
class TournamentSettings(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'creation_date', 'status', 'type', 'format', 'club', 'rounds'] 

class ImportCSVFile(forms.Form):
    ...


class RegisterParticipant(forms.ModelForm):
    class Meta: 
        mode = Participant
        fields = ['name', 'rating']