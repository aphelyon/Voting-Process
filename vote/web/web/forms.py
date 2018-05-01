from django import forms
from web import views
from web.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())

class VoterLoginForm(forms.Form):
    QRHash = forms.CharField(max_length=100, label = "Scan QR Code", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    firstname = forms.CharField(max_length = 100, label = "First Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    lastname = forms.CharField(max_length = 100, label = "Last Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    addr = forms.CharField(label = "Street Address", widget=forms.TextInput(attrs={'autocomplete':'off',}))

class VoterExitBoothForm(forms.Form):
    QRHash = forms.CharField(max_length=100, label = "Scan QR Code", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    firstname = forms.CharField(max_length = 100, label = "First Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    lastname = forms.CharField(max_length = 100, label = "Last Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    addr = forms.CharField(label = "Street Address", widget=forms.TextInput(attrs={'autocomplete':'off',}))

class RegistrationCheck(forms.Form):
    firstname = forms.CharField(max_length = 100, label = "First Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    lastname = forms.CharField(max_length = 100, label = "Last Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    addr = forms.CharField(label = "Street Address", widget=forms.TextInput(attrs={'autocomplete':'off',}))

class CandidateForm(forms.Form):
    firstname = forms.CharField(max_length=100, label="First Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    lastname = forms.CharField(max_length=100, label="Last Name", widget=forms.TextInput(attrs={'autocomplete':'off',}))
    dob = forms.DateField(label="Date of birth")

class ElectionForm(forms.Form):
    election_ID = forms.DateField(label="Election Date", input_formats=['%Y-%m'])
    election = (('General', 'General'), ('Primary', 'Primary'), ('Referendum', 'Referendum'))
    election_type = forms.CharField(label='Type of Election', widget=forms.Select(choices=election))

class AddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddForm, self, ).__init__(*args, **kwargs)
        candidate_items = []
        get_candidates = Candidate.objects.all()
        all_the_candidates = [candidate.as_json() for candidate in get_candidates]
        for candidate in all_the_candidates:
            pk = candidate['pk']
            candidates = candidate['first_name'] + " " + candidate['last_name'] + " " + str(candidate['dob'].year)
            tuple = (pk, candidates)
            candidate_items.append(tuple)
        candidate_items.sort(key=lambda candidate: candidate[1])
        self.fields['candidate'] = forms.Field(widget=forms.Select(choices=candidate_items))
        election_items = []
        get_election = Election.objects.all()
        all_the_elections = [election.as_json() for election in get_election]
        for election in all_the_elections:
            pk = election['pk']
            elections = election['election_id']
            tuple = (pk, elections)
            election_items.append(tuple)
        election_items.sort(key=lambda election: election[1])
        self.fields['election'] = forms.CharField(widget=forms.Select(choices=election_items))
        self.fields['position'] = forms.CharField(max_length=100, label="Position")
        self.fields['party'] = forms.CharField(max_length=100, label="Party")
        self.fields['precinct_id'] = forms.CharField(max_length=15, label="Precinct ID")

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
        election_items.sort(key=lambda election: election[1])
        self.fields['election'] = forms.CharField(widget=forms.Select(choices=election_items))
        self.fields['precinct_id'] = forms.CharField(max_length=15)

class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.form_position = kwargs.pop('form_position')
        self.ballot_entries = kwargs.pop('ballot_entries')
        super(VoteForm, self).__init__(*args, **kwargs)
        ballot_entry_items = []
        for ballot_entry in self.ballot_entries:
            if self.form_position == ballot_entry.position:
                pk = ballot_entry.candidate_id
                c = Candidate.objects.get(pk=pk)
                candid = c.first_name + " " + c.last_name
                tuple = (pk, candid)
                ballot_entry_items.append(tuple)
        ballot_entry_items.sort(key=lambda candidate: candidate[1])
        tuple = ('ABSTAIN', 'I abstain from voting for a ' + str(self.form_position))
        ballot_entry_items.append(tuple)
        self.fields[self.form_position] = forms.CharField(widget=forms.RadioSelect(choices=ballot_entry_items, attrs={'size':'30'}))
        self.initial[self.form_position] = ballot_entry_items[-1]


class SampleVoteForm(forms.Form):
    list_of_candidates = [(0, 'George Washington'),(1,'Abraham Lincoln'),(2,'Thomas Jefferson')]
    candidates = forms.CharField(widget=forms.RadioSelect(choices=list_of_candidates, attrs={'size':'30'}))

class MediaForm(forms.Form):
    company_name = forms.CharField(max_length=100, label="Company name")


class DeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.ballot_entries = kwargs.pop('ballot_entries')
        super(DeleteForm, self).__init__(*args, **kwargs)
        ballot_entry_items = []
        for ballot_entry in self.ballot_entries:
            pk = ballot_entry.pk
            c = Candidate.objects.get(pk=ballot_entry.candidate_id)
            ballot = c.first_name + " " + c.last_name + " " + str(c.dob.year) + " " + ballot_entry.position
            tuple = (pk, ballot)
            ballot_entry_items.append(tuple)
        ballot_entry_items.sort(key=lambda ballot: ballot[1])
        self.fields['ballot_entry'] = forms.CharField(widget=forms.Select(choices=ballot_entry_items))
