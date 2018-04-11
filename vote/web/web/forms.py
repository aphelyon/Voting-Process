from django import forms
from web import views
from web.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())

class VoterLoginForm(forms.Form):
    QRCode = forms.CharField(max_length=16, label = "Scan QR Code")
    dob = forms.CharField(max_length = 20, label = "Date of Birth")

class RegistrationCheck(forms.Form):
    firstname = forms.CharField(max_length = 100, label = "First Name")
    lastname = forms.CharField(max_length = 100, label = "Last Name")
    dob = forms.CharField(label = "Date of Birth")

class CandidateForm(forms.Form):
    firstname = forms.CharField(max_length=100, label="First Name")
    lastname = forms.CharField(max_length=100, label="Last Name")
    dob = forms.DateField(label="Date of birth")
    party = forms.CharField(max_length=100, label="Party")
    position = forms.CharField(max_length=100, label="Position")

class ElectionForm(forms.Form):
    election_ID = forms.DateField(label="Election Date", input_formats=['%Y-%m'])
    election = (('Primary', 'Primary'), ('General', 'General'), ('Referendum', 'Referendum'))
    election_type = forms.CharField(label='Type of Election', widget=forms.Select(choices=election))

class AddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddForm, self, ).__init__(*args, **kwargs)
        candidate_items = []
        get_candidates = Candidate.objects.all()
        all_the_candidates = [candidate.as_json() for candidate in get_candidates]
        for candidate in all_the_candidates:
            pk = candidate['pk']
            candidates = candidate['first_name'] + " " + candidate['last_name']
            tuple = (pk, candidates)
            candidate_items.append(tuple)
        self.fields['candidate'] = forms.Field(widget=forms.Select(choices=candidate_items))
        election_items = []
        get_election = Election.objects.all()
        all_the_elections = [election.as_json() for election in get_election]
        for election in all_the_elections:
            pk = election['pk']
            elections = election['election_id']
            tuple = (pk, elections)
            election_items.append(tuple)
        self.fields['election'] = forms.CharField(widget=forms.Select(choices=election_items))

class ElectionSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ElectionSelectionForm, self, ).__init__(*args, **kwargs)
        election_items = []
        get_election = Election.objects.all()
        all_the_elections = [election.as_json() for election in get_election]
        for election in all_the_elections:
            pk = election['pk']
            elections = election['election_id']
            tuple = (pk, elections)
            election_items.append(tuple)
        self.fields['election'] = forms.CharField(widget=forms.Select(choices=election_items))

class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.positions = kwargs.pop('positions')
        self.candidates = kwargs.pop('candidates')
        super(VoteForm, self).__init__(*args, **kwargs)
        for position in self.positions:
            candidate_items = []
            for candidate in self.candidates:
                if position == candidate.position:
                    pk = candidate.pk
                    candid = candidate.first_name + " " + candidate.last_name
                    tuple = (pk, candid)
                    candidate_items.append(tuple)
            self.fields[position] = forms.CharField(widget=forms.RadioSelect(choices=candidate_items))
