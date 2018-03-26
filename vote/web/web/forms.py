from django import forms
from web import views

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())

class RegistrationCheck(forms.Form):
    firstname = forms.CharField(max_length = 100, label = "First Name")
    lastname = forms.CharField(max_length = 100, label = "Last Name")
    dob = forms.CharField(max_length = 20, label = "Date of birth")
    ssn = forms.CharField(max_length = 4, label = "Last 4 digits of SSN")

