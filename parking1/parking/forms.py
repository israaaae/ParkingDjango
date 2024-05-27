from django import forms
from .models import ParkingEntry, ParkingExit, Vehicle
from django import forms
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['matricule']


class ParkingEntryForm(forms.ModelForm):
    class Meta:
        model = ParkingEntry
        fields = ['vehicle', 'location', 'status']


class ParkingExitForm(forms.ModelForm):
    parking_entry = forms.ModelChoiceField(queryset=ParkingEntry.objects.filter(status='Entrant'))

    class Meta:
        model = ParkingExit
        fields = ['parking_entry']
