from django import forms
from web import views

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())

class VoterLoginForm(forms.Form):
    QRCode = forms.CharField(max_length=16, label = "Scan QR Code")
    dob = forms.CharField(max_length = 20, label = "Date of Birth")

class RegistrationCheck(forms.Form):
    firstname = forms.CharField(max_length = 100, label = "First Name")
    lastname = forms.CharField(max_length = 100, label = "Last Name")
    dob = forms.DateField(label = "Date of Birth")

class CandidateForm(forms.Form):
    firstname = forms.CharField(max_length=100, label="First Name")
    lastname = forms.CharField(max_length=100, label="Last Name")
    dob = forms.DateField(label="Date of birth")
    party = forms.CharField(max_length=100, label="Party")

class ElectionForm(forms.Form):
    election_ID = forms.DateField(label="Election Date", input_formats=['%Y-%m'])
    election = (('Primary', 'Primary'), ('General', 'General'), ('Referendum', 'Referendum'))
    election_type = forms.CharField(label='Type of Election', widget=forms.Select(choices=election))

class AddForm(forms.Form):
    position = forms.CharField(max_length=100, label="Position")
    candidateID = forms.IntegerField(label="Candidate ID")
