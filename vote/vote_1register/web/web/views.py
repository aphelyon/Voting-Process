from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader
import urllib.request
import json
from web import models



def registration_check(request):
    return render(request, 'registration_check.html')
   
#there should be some sort of login for poll worker (using database) and super poll worker (admin). so that they can access the site.



#Voter registration information cataloging
def fetch_voter_info(precinct_id, api_key):
	try:
		req = urllib.request.Request('http://cs3240votingproject.org/pollingsite/'+ str(precinct_id) + + '/?key=' + str(api_key))
	except e:
		return error("Failed to fetch voter information.")

	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	return success(resp) 

def store_voter_info(precinct_id, api_key):	
	resp = fetch_voter_info(precinct_id, api_key)

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
