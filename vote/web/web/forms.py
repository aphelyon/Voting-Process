from django import forms
from web import views

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())

class RegistrationCheck(forms.Form):
    firstname = forms.CharField(max_length = 100, label = "First Name")
    lastname = forms.CharField(max_length = 100, label = "Last Name")
    dob = forms.CharField(max_length = 20, label = "Date of Birth")
    ssn = forms.CharField(max_length = 4, label = "Last 4 digits of SSN")

class CandidateForm(forms.Form):
    firstname = forms.CharField(max_length=100, label="First Name")
    lastname = forms.CharField(max_length=100, label="Last Name")
    dob = forms.DateField(label="Date of birth")
    party = forms.CharField(max_length=100, label="Party")

class ElectionForm(forms.Form):
    election_date = forms.DateField(label="Election Date", input_formats=['%Y-%m'])
    election = (('Primary', 'Primary'), ('General', 'General'), ('Referendum', 'Referendum'))
    election_type = forms.CharField(label='Type of Election', widget=forms.Select(choices=election))

class AddForm(forms.Form):
    position = forms.CharField(max_length=100, label="Position")