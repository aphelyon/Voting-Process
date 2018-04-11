from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import resolve
import urllib.request
import json
from web import models
from web.models import *
import web.forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.forms.models import model_to_dict


def login(request):
    if request.user.is_authenticated:
        return registration_check(request)
    form = web.forms.LoginForm()
    if request.method in ["POST", "GET"]:
        return auth_views.login(request, 'login.html')

def voter_login(request):
    form = web.forms.VoterLoginForm()
    if request.method == "GET":
        return render(request, 'voter_login.html', {'form':form})

def instructions1(request):
    return render(request,'instructions1.html')

def instructions2(request):
    return render(request,'instructions2.html')

def overview(request):
    return render(request,'overview.html')

def voter_finished(request):
    return render(request,'voter_finished.html')

@login_required
def registration_check(request):
    form = web.forms.RegistrationCheck()
    if request.method == "GET":
        return render(request, 'registration_check.html', {'form': form})

    sample_voter = {"fn":"john", "ln": "doe", "dob": "01/01/1970"}

    f = web.forms.RegistrationCheck(request.POST)
    if not f.is_valid():
        return render(request, 'registration_check.html', {'form': f})
    first_name = f.cleaned_data['firstname']
    last_name = f.cleaned_data['lastname']
    dob = f.cleaned_data['dob']
    if (sample_voter["fn"] == first_name) and (sample_voter["ln"] == last_name) and (sample_voter["dob"] == dob):
        return voter_registered(request)
    else:
        return voter_not_registered(request)

@login_required
def voter_registered(request):
    return render(request, 'voter_registered.html')

@login_required
def voter_not_registered(request):
    return render(request, 'voter_not_registered.html')

@login_required
def create_candidate(request):
    form = web.forms.CandidateForm()
    if request.method == "GET":
        return render(request, 'create_candidate.html', {'form': form})
    f = web.forms.CandidateForm(request.POST)
    if not f.is_valid():
        return render(request, 'create_candidate.html', {'form': f})
    first_name = f.cleaned_data['firstname']
    last_name = f.cleaned_data['lastname']
    dob = f.cleaned_data['dob']
    get_candidates = Candidate.objects.all()
    all_the_candidates = [candidate.as_json() for candidate in get_candidates]
    failure = False
    for candidate in all_the_candidates:
        if first_name == candidate['first_name'] and last_name == candidate['last_name']  and dob == candidate['dob']:
            failure = True
    if failure:
        response = {'ok': False, 'error_msg': "Candidate already exists", 'form': form}
        return render(request, 'create_candidate.html', response)
    new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, dob=dob)
    response = {"Status": "200", 'ok': True, "candidate": new_candidate.as_json(), 'form': form, 'success_msg': "Candidate was successfully created"}
    return render(request, 'create_candidate.html', response)

@login_required
def create_election(request):
    form = web.forms.ElectionForm()

    if request.method == "GET":
        return render(request, 'create_election.html', {'form': form})

    f = web.forms.ElectionForm(request.POST)
    if not f.is_valid():
        response = {'form': f, 'ok': False, 'error_msg': "Date Format is invalid"}
        return render(request, 'create_election.html', response)
    election_ID = f.cleaned_data['election_ID']
    electType = f.cleaned_data['election_type']
    month = election_ID.month
    year = election_ID.year
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    if month < 10:
        electionID = "" + str(year) + "-0" + str(month)
    else:
        electionID = "" + str(year) + "-" + str(month)
    failure = False
    for election in all_the_elections:
        if electionID == election['election_id']:
            failure = True
    if failure:
        response = {'form': f, 'ok': False, 'error_msg': "Election already exists"}
        return render(request, 'create_election.html', response)
    new_election = Election.objects.create(election_id=electionID, election_type=electType)
    response = {"Status": "200", "Election": new_election.as_json(), 'ok': True, 'success_msg': "Election was successfully created", 'form': form}
    return render(request, 'create_election.html', response)

@login_required
def create_ballot_entry(request):
    form = web.forms.AddForm()
    if request.method == "GET":
        return render(request, 'add_candidate.html', {'form': form})
    f = web.forms.AddForm(request.POST)
    if not f.is_valid():
        return render(request, 'add_candidate.html', {'form': f})
    position = f.cleaned_data['position']
    party = f.cleaned_data['party']
    election = f.cleaned_data['election']
    candidate = f.cleaned_data['candidate']
    num_votes = 0
    get_ballot_entries = BallotEntry.objects.all()
    ballot = [ballot_entry.as_json() for ballot_entry in get_ballot_entries]
    failure = False
    for ballot_entry in ballot:
        if position == ballot_entry['position'] and party == ballot_entry['party'] and election == ballot_entry['election_id'] and candidate == str(ballot_entry['candidate_id']):
            failure = True
    if failure:
        response = {'ok': False, 'error_msg': "Ballot entry already exists", 'form': form}
        return render(request, 'add_candidate.html', response)
    new_ballot_entry = BallotEntry.objects.create(election_id=election, candidate_id=candidate, num_votes=num_votes, party=party, position=position)
    e = Election.objects.get(pk=election)
    c = Candidate.objects.get(pk=candidate)
    e.ballotEntries.add(new_ballot_entry)
    c.ballotEntries.add(new_ballot_entry)
    response = {"Status": "200", 'ok': True, 'success_msg': "Ballot Entry was successfully created", 'form': form, 'Ballot_Entry': new_ballot_entry.as_json()}
    return render(request, 'add_candidate.html', response)

def elections(request):
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    return JsonResponse({'elections': all_the_elections})

def candidates(request):
    get_candidates = Candidate.objects.all()
    all_the_candidates = [candidate.as_json() for candidate in get_candidates]
    return JsonResponse({'candidates': all_the_candidates})

#There should be some sort of login for poll worker (using database) and super poll worker (admin). so that they can access the site.

def election_details(request, year, month):
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    success = False
    for election in all_the_elections:
        if str(election['election_id']) == str(year) + "-" + str(month) or str(election['election_id']) == str(year) + "-0" + str(month):
            success = True
            election_id = str(election['election_id'])
    if (success):
        election_object = Election.objects.get(election_id=election_id)
        positions = []
        ballot_entries = []
        position_dictionary = {}
        for ballot_entry in election_object.ballotEntries.all():
            ballot_entries.append(ballot_entry)
            if ballot_entry.position not in positions:
                positions.append(ballot_entry.position)
        for position in positions:
            ballotEntries = []
            for ballot_entry in election_object.ballotEntries.all():
                if position == ballot_entry.position:
                    c = Candidate.objects.get(pk=ballot_entry.candidate_id)
                    candid = dict(first_name=c.first_name, last_name=c.last_name, num_votes=ballot_entry.num_votes,
                         party=ballot_entry.party)
                    ballotEntries.append(candid)
            position_dictionary[position] = ballotEntries
        return JsonResponse({'success': success, 'positions': position_dictionary})
    else:
        return render(request, 'failure.html')

def election_selection(request):
    form = web.forms.ElectionSelectionForm()
    if request.method == "GET":
        return render(request, 'election_selection.html', {'form': form})
    f = web.forms.ElectionSelectionForm(request.POST)
    if not f.is_valid():
        return render(request, 'election_selection.html', {'form': f})
    election = f.cleaned_data['election']
    request.session['election'] = election
    return render(request, 'election_selection.html', {'form': f, 'success_msg': "The current election has been set to " + election})

def vote(request):
    if 'election' in request.session:
        election = request.session['election']
    elect = Election.objects.get(election_id=election)
    positions = []
    ballot_entries = []
    for ballot_entry in elect.ballotEntries.all():
        ballot_entries.append(ballot_entry)
        if ballot_entry.position not in positions:
            positions.append(ballot_entry.position)
    form = web.forms.VoteForm(ballot_entries=ballot_entries, positions=positions)
    if request.method == "GET":
        return render(request, 'vote.html', {'form': form})
    f = web.forms.VoteForm(request.POST, ballot_entries=ballot_entries, positions=positions)
    if not f.is_valid():
        return render(request, 'vote.html', {'form': f})
    voted_ballot_entries = []
    for position in positions:
        candidate_pk = f.cleaned_data[position]
        for ballot_entry in elect.ballotEntries.all():
            if str(ballot_entry.candidate_id) == str(candidate_pk):
                ballot_entry.num_votes += 1
                ballot_entry.save()
                candidate = Candidate.objects.get(pk=candidate_pk)
                voted_ballot_entries.append(candidate.first_name + " " + candidate.last_name + " " + str(ballot_entry.num_votes))
    response = {"Status": "200", 'candidates': voted_ballot_entries}
    return JsonResponse({'ok': True, 'results': response})

#Voter registration information cataloging
def fetch_voter_info(precinct_id, api_key):

	#Try to query the voter registration database.
	try:
		req = urllib.request.Request('http://cs3240votingproject.org/pollingsite/'+ str(precinct_id) + + '/?key=' + str(api_key))
	except e:
		return error("Failed to fetch voter information.")

	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	#Return information as a dictionary
	return success(resp)


#Store voter information in the local database.
def store_voter_info(precinct_id, api_key):
	#Fetch voter information
	resp = fetch_voter_info(precinct_id, api_key)


	#Store voter information if it worked.
	if resp["status"]:
		voters = resp["data"]["voters"]
		for i in range(len(voters)):
			info = voters[i]
			info["zipcode"] = info["zip"]
			info.pop("zip", None)
			voter = models.Voter( **info )
			try:
				voter.save()
			except:
				return error("Failed to save some voter information to the local database.")
		return success()
	else:
		return resp


#Helper methods
def error(err_msg):
    return {'status': False, 'error': err_msg}

def success(data = None):
    if data:
    	return {'status': True, 'data': data}
    else:
    	return {'status': True}
