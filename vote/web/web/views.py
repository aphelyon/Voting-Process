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


def login(request):
    form = web.forms.LoginForm()
    if request.method == "GET":
        return render(request, 'login.html', {'form': form})

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
        return render(request, 'voterregistered.html')
    else:
        return render(request, 'voternotregistered.html')

@login_required
def voterregistered(request):
    form = web.forms.RegistrationCheck()
    if request.method == "GET":
        return render(request, 'voterregistered.html', {'form': form})

@login_required
def voternotregistered(request):
    form = web.forms.RegistrationCheck()
    if request.method == "GET":
        return render(request, 'voternotregistered.html', {'form': form})

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
    party= f.cleaned_data['party']
    dob = f.cleaned_data['dob']
    num_votes = 0
    new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, num_votes=num_votes, party=party, dob=dob)
    response = {"Status": "200", "candidate": new_candidate.as_json()}
    return JsonResponse({'ok': True, 'results': response})

@login_required
def create_election(request):
    form = web.forms.ElectionForm()

    if request.method == "GET":
        return render(request, 'create_election.html', {'form': form})

    f = web.forms.ElectionForm(request.POST)
    if not f.is_valid():
        return render(request, 'create_election.html', {'form': f})
    election_ID = f.cleaned_data['election_ID']
    electType = f.cleaned_data['election_type']
    month = election_ID.month
    year = election_ID.year
    if month < 10:
        electionID = "" + str(year) + "-0" + str(month)
    else:
        electionID = "" + str(year) + "-" + str(month)
    new_election = Election.objects.create(election_id=electionID, election_type=electType)
    response = {"Status": "200", "Election": new_election.as_json()}
    return JsonResponse({'ok': True, 'results': response})

@login_required
def add_candidate(request):
    form = web.forms.AddForm()
    if request.method == "GET":
        return render(request, 'add_candidate.html', {'form': form})

def elections(request):
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    return JsonResponse({'elections': all_the_elections})

def candidates(request):
    get_candidates = Candidate.objects.all()
    all_the_candidates = [candidate.as_json() for candidate in get_candidates]
    return JsonResponse({'candidates': all_the_candidates})

#There should be some sort of login for poll worker (using database) and super poll worker (admin). so that they can access the site.

def election_stuff(request, year, month):
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    success = False
    for election in all_the_elections:
        if str(election['election_id']) == str(year) + "-" + str(month) or str(election['election_id']) == str(year) + "-0" + str(month):
            success = True
    if (success):
        return JsonResponse({'success': success})
    else:
        return render(request, 'failure.html')



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
