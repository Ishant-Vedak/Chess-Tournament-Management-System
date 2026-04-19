from django import forms
from .models import Tournament, Participant

class CreateTournament(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "format", 'club']
        labels = {
            'name': 'Tournament Name',
            'format': 'Tournament Format',
            'club': 'Organizer Club',
        }
    
class TournamentSettings(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'creation_date', 'status', 'format', 'club', 'rounds'] 
        labels = {
            'name': 'Tournament Name',
            'creation_date': 'Creation Date',
            'status': 'Tournament Status',
            'format': 'Tournament Format',
        }

class RegisterParticipant(forms.ModelForm):
    class Meta: 
        model = Participant
        fields = ['name', 'second_name', 'email', 'cfc_rating', 'fide_rating']
        labels = {
            'name': 'First Name',
            'second_name': 'Last Name',
            'email': 'Email',
            'cfc_rating': 'CFC Rating',
            'fide_rating': 'FIDE Rating',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Magnus'}),
            'second_name': forms.TextInput(attrs={'placeholder': 'e.g. Carlsen'}),
        }
