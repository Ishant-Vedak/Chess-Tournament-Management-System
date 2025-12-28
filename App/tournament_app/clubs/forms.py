from django import forms
from .models import Club

class CreateClub(forms.ModelForm):
    
    club_name = forms.CharField(label='Club Name', max_length=100)
    website = forms.URLField(label='Club Website')
    
    class Meta:
        model = Club
        fields = ("club_name", "website")

    