from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader
import urllib.request
import json
from web import models
import web.forms
from django.contrib.auth.decorators import login_required

def login(request):
    form = web.forms.LoginForm()
    if request.method == "GET":
        return render(request, 'login.html', {'form': form})

@login_required
def registration_check(request):
    form = web.forms.RegistrationCheck()
    if request.method == "GET":
        return render(request, 'registration_check.html', {'form': form})

@login_required
def create_candidate(request):
    form = web.forms.CandidateForm()
    if request.method == "GET":
        return render(request, 'create_candidate.html', {'form': form})

@login_required
def create_election(request):
    form = web.forms.ElectionForm()
    if request.method == "GET":
        return render(request, 'create_election.html', {'form': form})



#There should be some sort of login for poll worker (using database) and super poll worker (admin). so that they can access the site.




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
