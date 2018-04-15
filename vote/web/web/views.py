from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import resolve
import urllib.request
import json
import hashlib
from web import models
from web.models import *
import web.forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.forms.models import model_to_dict
import qrcode
import io

def login(request):
    if request.method == "POST":
        fetch_and_store_voter_info("0405","12345")
    if request.user.is_authenticated:
        return HttpResponseRedirect("/registration_check/")
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

    f = web.forms.RegistrationCheck(request.POST)
    if not f.is_valid():
        return render(request, 'registration_check.html', {'form': f})
    fn_entered = f.cleaned_data['firstname']
    ln_entered = f.cleaned_data['lastname']
    dob_entered = f.cleaned_data['dob']

    try:
        db_voter = Voter.objects.get(first_name=fn_entered, last_name=ln_entered)
    except:
        return render(request, "voter_not_registered.html")
    return voter_registered(request, fn_entered, ln_entered, dob_entered)

def voter_registered(request, fn, ln, dob):
    h = hashlib.md5()
    h.update((fn + ln + dob).encode('utf-8')) # going to need to hash the election id as well
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=39,
        border=4,
    )        


    img_data = qrcode.make(h.hexdigest()) #THIS RETURNS THE QR CODE AS AN IMAGE! doesn't return a template. 
                                          #need to find a way to fix this.
    response = HttpResponse(content_type="image/png")
    img_data.save(response, "PNG")
    return response       
    #return render(request, 'voter_registered.html', {'fn':fn, 'ln':ln, 'hash':h.hexdigest()})

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
    position = f.cleaned_data['position']
    dob = f.cleaned_data['dob']
    num_votes = 0
    get_candidates = Candidate.objects.all()
    all_the_candidates = [candidate.as_json() for candidate in get_candidates]
    failure = False
    for candidate in all_the_candidates:
        if first_name == candidate['first_name'] and last_name == candidate['last_name'] and position == candidate['position'] and dob == candidate['dob']:
            failure = True
    if failure:
        return JsonResponse({'ok': False, 'error_msg': "Candidate under this position already exists"})
    new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, num_votes=num_votes, party=party, dob=dob, position=position)
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
    f = web.forms.AddForm(request.POST)
    if not f.is_valid():
        return render(request, 'add_candidate.html', {'form': f})
    election = f.cleaned_data['election']
    candidate = f.cleaned_data['candidate']
    e = Election.objects.get(pk=election)
    c = Candidate.objects.get(pk=candidate)
    e.candidates.add(c)
    candid = []
    candidates = e.candidates.all()
    for candidat in candidates:
        candid.append(candidat.first_name + " " + candidat.last_name)
    response = {"Status": "200", "Election": e.as_json(), "candidates": candid}
    return JsonResponse({'ok': True, 'results': response})


def elections(request):
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    return JsonResponse({'elections': all_the_elections})

def candidates(request):
    get_candidates = Candidate.objects.all()
    all_the_candidates = [candidate.as_json() for candidate in get_candidates]
    return JsonResponse({'candidates': all_the_candidates})

def voters(request):
    get_voters = Voter.objects.all()
    all_the_voters = [voter.as_json() for voter in get_voters]
    return JsonResponse({'count': len(all_the_voters), 'voters': all_the_voters})

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
        candidates = []
        position_dictionary = {}
        for candidate in election_object.candidates.all():
            candidates.append(candidate)
            if candidate.position not in positions:
                positions.append(candidate.position)
        for position in positions:
            candidates = []
            for candidate in election_object.candidates.all():
                if position == candidate.position:
                    candid = dict(first_name=candidate.first_name, last_name=candidate.last_name, num_votes=candidate.num_votes,
                         party=candidate.party)
                    candidates.append(candid)
            position_dictionary[position] = candidates
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
    return JsonResponse({'success': True})

def vote(request):
    if 'election' in request.session:
        election = request.session['election']
    elect = Election.objects.get(election_id=election)
    positions = []
    candidates = []
    for candidate in elect.candidates.all():
        candidates.append(candidate)
        if candidate.position not in positions:
            positions.append(candidate.position)
    form = web.forms.VoteForm(candidates=candidates, positions=positions)
    if request.method == "GET":
        return render(request, 'vote.html', {'form': form})
    f = web.forms.VoteForm(request.POST, candidates=candidates, positions=positions)
    if not f.is_valid():
        return render(request, 'vote.html', {'form': f})
    voted_candidates = []
    for position in positions:
        candidate_pk = f.cleaned_data[position]
        for candidate in elect.candidates.all():
            if str(candidate.pk) == str(candidate_pk):
                candidate.num_votes += 1
                candidate.save()
                voted_candidates.append(candidate.first_name + " " + candidate.last_name + " " + str(candidate.num_votes))
    response = {"Status": "200", 'candidates': voted_candidates}
    return JsonResponse({'ok': True, 'results': response})

#Voter registration information cataloging
def fetch_voter_info(precinct_id, api_key):

	#Try to query the voter registration database.
	try:
		req = urllib.request.Request('http://people.virginia.edu/~esm7ky/precinct1.json')
        # req = urllib.request.Request('http://people.virginia.edu/~esm7ky/precinct.json')
	except e:
		return error("Failed to fetch voter information.")

	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	#Return information as a dictionary
	return success(resp)


#Store voter information in the local database.
def fetch_and_store_voter_info(precinct_id, api_key):
    # Remove all voters currently in database
    Voter.objects.all().delete()
	# Fetch voter information
    resp = fetch_voter_info(precinct_id, api_key)

	#Store voter information if it worked.
    if resp["status"]:
        voters = resp["data"]["voters"]
        for i in range(len(voters)):
            info = voters[i]
            info["zipcode"] = info["zip"]
            info.pop("zip", None)
            voter = Voter.objects.create( **info )
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
