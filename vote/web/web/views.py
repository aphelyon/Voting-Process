from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import resolve, reverse
import urllib.request
import json
import hashlib
from web import models
from web.models import *
import web.forms
from copy import deepcopy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.forms.models import model_to_dict
import qrcode
import io
from binascii import hexlify
import os
from queue import Queue

q = Queue()

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/registration_check")
    form = web.forms.LoginForm()
    if request.method in ["POST", "GET"]:
        request.session['precinct_list'] = get_all_precincts()
        return auth_views.login(request, 'login.html')

@login_required
def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("../login")
    keys_to_store = ["election", "election_type", "precinct_id"]
    temp_obj = {}
    for key in keys_to_store:
        if key in request.session:
            temp_obj[key] = deepcopy(request.session[key])
    auth_views.logout(request)
    for key in temp_obj:
        request.session[key] = deepcopy(temp_obj[key])
    return redirect("../login")

def voter_login(request):
    form = web.forms.VoterLoginForm()
    if request.method == "GET":
        return render(request, 'voter_login.html', {'form':form})

    f = web.forms.VoterLoginForm(request.POST)
    if not f.is_valid():
        return render(request, 'voter_login.html', {'form': f})
    qr_entered = f.cleaned_data['QRHash']
    fn_entered = f.cleaned_data['firstname']
    ln_entered = f.cleaned_data['lastname']
    addr_entered = f.cleaned_data['addr']
    cur_election = request.session['election']

    h = hashlib.sha256()
    h.update((fn_entered + ln_entered + addr_entered + cur_election).encode('utf-8')) # going to need to hash the election id as well
    cur_hash = h.hexdigest()

    try:
        db_anon_voter = AnonVote.objects.get(hash=cur_hash)
        request.session['auth'] = False
        request.session['hash'] = ''
        nex = reverse('already_voted')
        response = HttpResponseRedirect(nex)
        return response
    except:
        pass

    if cur_hash == qr_entered:
        request.session['auth'] = True
        request.session['hash'] = qr_entered
        nex = reverse('instructions1')
        response = HttpResponseRedirect(nex)
        return response
    else:
        request.session['auth'] = False
        nex = reverse('voter_login')
        response = HttpResponseRedirect(nex)
        return response

# This is a decorator definition to make sure that voters can only access
# voting-process-associated pages once they've been successfully authorized
def voter_auth(f):
    def wrap(request, *args, **kwargs):
        if "auth" in request.session and request.session["auth"]:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('../voter_login')
    return wrap

@voter_auth
def instructions1(request):
    form = web.forms.SampleVoteForm()
    if request.method == "GET":
        return render(request,'instructions1.html', {'form': form})
    if 'next' in request.POST:
        return redirect('../instructions2')

@voter_auth
def instructions2(request):
    if request.method == "GET":
        return render(request,'instructions2.html')
    if 'next' in request.POST:
        if request.session['election_type'] == "Primary":
            return redirect('../primary_party_select')
        else:
            return redirect('../vote/0')

@voter_auth
def primary_party_select(request):
    if request.method == "GET":
        return render(request, 'primary_party_select.html')
    if 'next' in request.POST:
        request.session['primary_party'] = request.POST.get("primary_party")
        return redirect('../vote/0')

@voter_auth
def voter_finished(request):
    request.session["auth"] = False
    request.session["hash"] = ""
    return render(request, "voter_finished.html")

@voter_auth
def voter_cancelled(request):
    request.session["auth"] = False
    request.session["hash"] = ""
    return render(request, "voter_cancelled.html")

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
    addr_entered = f.cleaned_data['addr']
    status = "active"

    try:
        db_voter = Voter.objects.get(first_name=fn_entered, last_name=ln_entered, street_address=addr_entered, voter_status=status)
    except:
        return render(request, "voter_not_registered.html")
    return voter_registered(request, fn_entered, ln_entered, addr_entered)

@login_required
def address_lookup(request):
    form = web.forms.AddressLookupForm()
    if request.method == "GET":
        return render(request, 'address_lookup.html', {'form': form, 'ok': True})

    f = web.forms.AddressLookupForm(request.POST)
    if not f.is_valid():
        return render(request, 'address_lookup.html', {'form': form, 'ok': True})
    fn_entered = f.cleaned_data['firstname']
    ln_entered = f.cleaned_data['lastname']

    try:
        db_voter = Voter.objects.get(first_name=fn_entered, last_name=ln_entered)
        return render(request, 'address_lookup.html', {'form': form, 'ok': True, 'addresses': [db_voter.street_address]})
    except:
        pass

    try:
        name_matched_voter_addresses = []
        for db_voter in Voter.objects.all():
            if db_voter.first_name == fn_entered and db_voter.last_name == ln_entered:
                name_matched_voters.append(db_voter.street_address)
        if len(name_matched_voter_addresses) != 0:
            return render(request, 'address_lookup.html', {'form': form, 'ok': True, 'addresses': name_matched_voter_addresses})
        else:
            return render(request, 'address_lookup.html', {'form': form, 'ok': False})
    except:
        return render(request, 'address_lookup.html', {'form': form, 'ok': False})

def voter_registered(request, fn, ln, addr):
    h = hashlib.sha256()
    cur_election = request.session['election']
    h.update((fn + ln + addr + cur_election).encode('utf-8'))

    try:
        db_anon_voter = AnonVote.objects.get(hash=h.hexdigest())
        return render(request, "voter_not_registered.html")
    except:
        pass

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=39,
        border=4,
    )

    img_data = qrcode.make(h.hexdigest()) #THIS RETURNS THE QR CODE AS AN IMAGE! doesn't return a template.
                                          #need to find a way to fix this.
    img_data = img_data.resize((128, 128))
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
    dob = f.cleaned_data['dob']
    get_candidates = Candidate.objects.all()
    all_the_candidates = [candidate.as_json() for candidate in get_candidates]
    failure = False
    for candidate in all_the_candidates:
        if first_name == candidate['first_name'] and last_name == candidate['last_name'] and dob == candidate['dob']:
            failure = True
    if failure:
        response = {'ok': False, 'error_msg': "Candidate already exists", 'form': form}
        return render(request, 'create_candidate.html', response)
    new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, dob=dob)
    response = {'ok': True, 'success_msg': "Candidate was successfully created", 'form': form, 'candidate': new_candidate.as_json()}
    return render(request, 'create_candidate.html', response)

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
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    month = election_ID.month
    year = election_ID.year
    failure = False
    if month < 10:
        electionID = "" + str(year) + "-0" + str(month)
    else:
        electionID = "" + str(year) + "-" + str(month)
    for election in all_the_elections:
        if electionID == election['election_id']:
            failure = True
    if failure:
        response = {'ok': False, 'error_msg': "Election already exists", 'form': form}
        return render(request, 'create_election.html', response)
    new_election = Election.objects.create(election_id=electionID, election_type=electType)
    response = {'ok': True, 'success_msg': "Election was successfully created", 'form': form,
                'election': new_election.as_json()}
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
    precinct_id = f.cleaned_data['precinct_id']
    num_votes = 0
    get_ballot_entries = BallotEntry.objects.all()
    ballot = [ballot_entry.as_json() for ballot_entry in get_ballot_entries]
    failure = False
    for ballot_entry in ballot:
        if position == ballot_entry['position'] and party == ballot_entry['party'] and election == ballot_entry['election_id'] and candidate == str(ballot_entry['candidate_id']) and precinct_id == ballot_entry['precinct_id']:
            failure = True
    if failure:
        response = {'ok': False, 'error_msg': "Ballot entry already exists", 'form': form}
        return render(request, 'add_candidate.html', response)
    if precinct_id == "all":
        if "precinct_list" not in request.session:
            response = {'ok': False, 'error_msg': "List of precincts not yet fetched", 'form': form}
            return render(request, 'add_candidate.html', response)
        new_ballot_entries = []
        for p_id in request.session["precinct_list"]:
            new_ballot_entry = BallotEntry.objects.create(election_id=election, candidate_id=candidate, num_votes=num_votes, party=party, position=position, precinct_id=p_id)
            e = Election.objects.get(pk=election)
            c = Candidate.objects.get(pk=candidate)
            e.ballotEntries.add(new_ballot_entry)
            c.ballotEntries.add(new_ballot_entry)
            new_ballot_entries.append(new_ballot_entry.as_json())
        response = {"Status": "200", 'ok': True, 'success_msg': "Ballot Entries were successfully created", 'form': form, 'Ballot_Entries': new_ballot_entries}
    else:
        new_ballot_entry = BallotEntry.objects.create(election_id=election, candidate_id=candidate, num_votes=num_votes, party=party, position=position, precinct_id=precinct_id)
        e = Election.objects.get(pk=election)
        c = Candidate.objects.get(pk=candidate)
        e.ballotEntries.add(new_ballot_entry)
        c.ballotEntries.add(new_ballot_entry)
        response = {"Status": "200", 'ok': True, 'success_msg': "Ballot Entry was successfully created", 'form': form, 'Ballot_Entry': new_ballot_entry.as_json()}
    return render(request, 'add_candidate.html', response)

@login_required
def delete_ballot_entry(request):
    if 'election' in request.session:
        election = request.session['election']
    elect = Election.objects.get(election_id=election)
    ballot_entries = []
    for ballot_entry in elect.ballotEntries.all():
        ballot_entries.append(ballot_entry)
    form = web.forms.DeleteForm(ballot_entries=ballot_entries)
    if request.method == "GET":
        return render(request, 'delete_ballot_entry.html', {'form': form})
    f = web.forms.DeleteForm(request.POST, ballot_entries=ballot_entries)
    if not f.is_valid():
        return render(request, 'delete_ballot_entry.html', {'form': f})
    ballot_entry = f.cleaned_data['ballot_entry']
    ballot = BallotEntry.objects.get(pk=ballot_entry)
    position = ballot.position
    candidate = Candidate.objects.get(pk=ballot.candidate_id)
    election = Election.objects.get(pk=ballot.election_id)
    candidate.ballotEntries.remove(ballot)
    election.ballotEntries.remove(ballot)
    BallotEntry.objects.filter(pk=ballot_entry).delete()
    ballot_entries = []
    for ballot_entry in elect.ballotEntries.all():
        ballot_entries.append(ballot_entry)
    form = web.forms.DeleteForm(ballot_entries=ballot_entries)
    response = {"Status": "200", 'ok': True, 'success_msg': "The Ballot Entry " + candidate.first_name + " " + candidate.last_name + " " + str(candidate.dob.year) + " " + position + " was successfully deleted" , 'form': form}
    return render(request, 'delete_ballot_entry.html', response)

def elections(request, api_key):
    try:
        media = MediaID.objects.get(pk=api_key)
    except MediaID.DoesNotExist:
        media = None
    if media == None:
        return render(request, 'api_failure.html')
    get_elections = Election.objects.all()
    all_the_elections = [election.as_json() for election in get_elections]
    return JsonResponse({'elections': all_the_elections})

def candidates(request, api_key):
    try:
        media = MediaID.objects.get(pk=api_key)
    except MediaID.DoesNotExist:
        media = None
    if media == None:
        return render(request, 'api_failure.html')
    get_candidates = Candidate.objects.all()
    all_the_candidates = [candidate.as_json() for candidate in get_candidates]
    return JsonResponse({'candidates': all_the_candidates})

def voters(request, api_key):
    try:
        media = MediaID.objects.get(pk=api_key)
    except MediaID.DoesNotExist:
        media = None
    if media == None:
        return render(request, 'api_failure.html')
    get_voters = Voter.objects.all()
    all_the_voters = [voter.as_json() for voter in get_voters]
    return JsonResponse({'count': len(all_the_voters), 'voters': all_the_voters})

def vote_records(request, api_key):
    try:
        media = MediaID.objects.get(pk=api_key)
    except MediaID.DoesNotExist:
        media = None
    if media == None:
        return render(request, 'api_failure.html')
    get_anon_votes = AnonVote.objects.all()
    all_the_votes = [vote.as_json() for vote in get_anon_votes]
    return JsonResponse({'count': len(all_the_votes), 'hashes': all_the_votes})

def election_details(request, year, month, api_key):
    try:
        media = MediaID.objects.get(pk=api_key)
    except MediaID.DoesNotExist:
        media = None
    if media == None:
        return render(request, 'api_failure.html')
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
                         party=ballot_entry.party, precinct_id=ballot_entry.precinct_id)
                    ballotEntries.append(candid)
            position_dictionary[position] = ballotEntries
        return JsonResponse({'success': success, 'positions': position_dictionary})
    else:
        return render(request, 'failure.html')

def candidate_details(request, first_name, last_name, year, api_key):
    try:
        media = MediaID.objects.get(pk=api_key)
    except MediaID.DoesNotExist:
        media = None
    if media == None:
        return render(request, 'api_failure.html')
    get_ballot_entries = BallotEntry.objects.all()
    ballot = [ballot_entry.as_json() for ballot_entry in get_ballot_entries]
    success = False
    for ballot_entry in ballot:
        c = Candidate.objects.get(pk=ballot_entry['candidate_id'])
        if str(c.first_name) == str(first_name) and str(c.last_name) == str(last_name) and str(c.dob.year) == str(year):
            success = True
            candidate = c
    if (success):
        elections = []
        ballot_entries = []
        election_dictionary = {}
        for ballot_entry in candidate.ballotEntries.all():
            ballot_entries.append(ballot_entry)
            if ballot_entry.election_id not in elections:
                elections.append(ballot_entry.election_id)
        for election in elections:
            ballotEntries = []
            for ballot_entry in candidate.ballotEntries.all():
                if election == ballot_entry.election_id:
                    ballot_entry_display = dict(party=ballot_entry.party, position=ballot_entry.position, num_votes=ballot_entry.num_votes)
                    ballotEntries.append(ballot_entry_display)
            election_dictionary[election] = ballotEntries
        return JsonResponse({'success': success, 'Elections': election_dictionary})
    else:
        return render(request, 'failure_candidate.html')

def election_selection(request):
    selected = False
    if 'election' in request.session:
        election = request.session['election']
        selected = True
        current_election = "The current election is " + election
    form = web.forms.ElectionSelectionForm()
    if request.method == "GET":
        current_election = ""
        return render(request, 'election_selection.html', {'form': form, 'selected': selected, 'current_election': current_election})
    f = web.forms.ElectionSelectionForm(request.POST)
    if not f.is_valid():
        return render(request, 'election_selection.html', {'form': f})
    election = f.cleaned_data['election']
    precinct_id = f.cleaned_data['precinct_id']
    request.session['election'] = election
    request.session['precinct_id'] = precinct_id
    elect_obj = Election.objects.get(pk=election)
    request.session['election_type'] = elect_obj.election_type
    selected = False
    fetch_and_store_voter_info(precinct_id)
    return render(request, 'election_selection.html', {'form': f, 'success_msg': "The current election has been set to " + election, 'ok': True, 'selected': selected})

@voter_auth
def vote(request, pos_num):
    election = None
    election_type = None
    primary_party = None
    primary_blacklist = None
    if 'election' in request.session:
        election = request.session['election']

    if 'election_type' in request.session:
        election_type = request.session['election_type']
        if election_type == "Primary":
            primary_party = request.session['primary_party']
            if primary_party == "Democrat":
                primary_blacklist = "Republican"
            else:
                primary_blacklist = "Democrat"

    elect = Election.objects.get(election_id=election)
    positions = []
    position_numbers = []
    ballot_entries = []
    navbar_positions =[] #holds the positions as they should show up on the nav bar
    #filling positions and ballot_entries arrays
    for ballot_entry in elect.ballotEntries.all():
        if ballot_entry.precinct_id == request.session['precinct_id']:
            if (primary_blacklist == None) or (primary_blacklist != None and ballot_entry.party != primary_blacklist):
                ballot_entries.append(ballot_entry)
                if ballot_entry.position not in positions:
                    positions.append(ballot_entry.position)
                    #split the navbar positions at the .
                    split_array = ballot_entry.position.split(".")
                    navbar_positions.append(split_array[0])

    maxPosition = len(positions) - 1

    if pos_num == 0:
        submission_data = {}
        request.session['submission'] = submission_data

    first_position = True
    if pos_num != 0:
        first_position = False
        submission_data = request.session['submission']

    last = False
    if pos_num == maxPosition:
        last = True

    confirm = False
    if pos_num == len(positions):
        confirm = True

    if not confirm:
        position = positions[pos_num]
        form = web.forms.VoteForm(ballot_entries=ballot_entries, form_position=position)

        if request.method == "GET":
            return render(request, 'vote.html',
                          {'form': form, 'first': first_position, 'last': last, 'positions': positions, 'navbar_positions': navbar_positions})
        f = web.forms.VoteForm(request.POST, ballot_entries=ballot_entries, form_position=position)
        if not f.is_valid():
            return render(request, 'vote.html',
                          {'form': f, 'first': first_position, 'last': last, 'positions': positions, 'navbar_positions': navbar_positions})

    if confirm:
        if request.method == "GET":
            not_voted =[]
            voted = []
            not_voted_flag = False
            count = 0
            allowed = False
            for position in positions:
                if str(count) not in submission_data:
                    not_voted.append(position)
                    voted.append("NOT VOTED FOR")
                    not_voted_flag = True
                else:
                    if submission_data[str(count)] == 'ABSTAIN':
                        voted.append(submission_data[str(count)])
                    else:
                        cur_cand = Candidate.objects.get(pk=submission_data[str(count)])
                        voted.append(cur_cand.first_name + " " + cur_cand.last_name)
                count += 1
            if len(submission_data) == len(positions):
                allowed = True
            return render(request, 'vote_confirm.html', {'form': submission_data, 'positions': positions, 'not_voted': not_voted, 'voted': voted, 'not_voted_flag': not_voted_flag, 'allowed': allowed})

    if 'next' in request.POST:
        submission_data[str(pos_num)] = f.cleaned_data[positions[pos_num]]
        request.session['submission'] = submission_data
        return redirect('../vote/' + str(pos_num + 1))

    if 'previous' in request.POST:
        if not confirm:
            submission_data[str(pos_num)] = f.cleaned_data[positions[pos_num]]
            request.session['submission'] = submission_data
        if pos_num == 0:
            return redirect('../instructions2')
        else:
            return redirect('../vote/' + str(pos_num - 1))

    if 'submit' in request.POST:
        submission_data[str(pos_num)] = f.cleaned_data[positions[pos_num]]
        request.session['submission'] = submission_data
        return redirect('../vote/' + str(pos_num + 1))

    if 'confirm' in request.POST:
        hash = str(request.session['hash'])
        try:
            db_anon_voter = AnonVote.objects.get(hash=hash)
            request.session['auth'] = False
            request.session['hash'] = ''
            return redirect('../already_voted')
        except:
            pass
        anon_vote = AnonVote.objects.create(hash=hash)
        count = 0
        vote_q = dict()
        vote_q["VOTER_HASH"]=request.session['hash']
        for position in positions:
            candidate_pk = submission_data[str(count)]
            if not candidate_pk == 'ABSTAIN':
                for ballot_entry in elect.ballotEntries.all():
                    if str(ballot_entry.candidate_id) == str(candidate_pk) and ballot_entry.position == position and ballot_entry.precinct_id == request.session["precinct_id"]:
                        ballot_entry.num_votes += 1
                        ballot_entry.save()
                        anon_vote.ballotEntries.add(ballot_entry)
                vote_q[position] = Candidate.objects.get(pk=candidate_pk).first_name + " " + Candidate.objects.get(pk=candidate_pk).last_name
            else:
                vote_q[position] = "ABSTAIN"
            count += 1
        q.put(vote_q)
        anon_vote.save()
        return redirect('../voter_finished')

def already_voted(request):
    return render(request,'already_voted.html')

def voter_exit_booth(request):
    form = web.forms.VoterExitBoothForm()
    if request.method == "GET":
        return render(request, 'voter_exit_booth.html', {'form':form})

    f = web.forms.VoterExitBoothForm(request.POST)
    if not f.is_valid():
        return render(request, 'voter_exit_booth.html', {'form': f})
    qr_entered = f.cleaned_data['QRHash']
    fn_entered = f.cleaned_data['firstname']
    ln_entered = f.cleaned_data['lastname']
    addr_entered = f.cleaned_data['addr']
    cur_election = request.session['election']

    h = hashlib.sha256()
    h.update((fn_entered + ln_entered + addr_entered + cur_election).encode('utf-8')) # going to need to hash the election id as well
    cur_hash = h.hexdigest()
    if cur_hash == qr_entered:
        request.session['hash'] = qr_entered
        request.session['exit_auth'] = True
        nex = reverse('vote_record')
        response = HttpResponseRedirect(nex)
        return response
    else:
        request.session['hash'] = ""
        request.session['exit_auth'] = False
        nex = reverse('voter_exit_booth')
        response = HttpResponseRedirect(nex)
        return response

# This is a decorator definition to make sure that voters can only access
# voting-confirmation page once they've been successfully authorized
def voter_exit_auth(f):
    def wrap(request, *args, **kwargs):
        if "exit_auth" in request.session and request.session["exit_auth"]:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('../voter_exit_booth')
    return wrap

@voter_exit_auth
def vote_record(request):
    hash = str(request.session['hash'])
    anon_vote = None
    try:
        anon_vote = AnonVote.objects.get(hash=hash)
    except:
        request.session['hash'] = ""
        request.session['exit_auth'] = False
        return HttpResponseRedirect('../voter_exit_booth')
    ballot_entries = anon_vote.ballotEntries.all()
    vote_tuples = []
    for ballot_entry in ballot_entries:
        position = ballot_entry.position
        cand_id = ballot_entry.candidate_id
        candidate = Candidate.objects.get(pk=cand_id)
        name = candidate.first_name + " " + candidate.last_name
        if ballot_entry.party != "Referendum":
            name = name + ", " + ballot_entry.party + " Party"
        vote_tuples.append((position, name))
    request.session['exit_auth'] = False
    request.session['hash'] = ""
    return render(request, "vote_record.html", {'vote_tuples': vote_tuples})

# querying the voter registration database to find the set of precincts
def get_all_precincts():
    try:
        req = urllib.request.Request('http://CS3240votingproject.org/voters/?key=goofy')
    except e:
        return error("Failed to fetch voter information.")
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    voters = resp["voters"]
    precinct_ids = []
    for i in range(len(voters)):
        precinct_id = voters[i]["precinct_id"]
        if precinct_id not in precinct_ids:
            precinct_ids.append(precinct_id)
    return precinct_ids

#Voter registration information cataloging
def fetch_voter_info(precinct_id):
	#Try to query the voter registration database.
	try:
		req = urllib.request.Request('http://CS3240votingproject.org/pollingsite/' + str(precinct_id) + "/?key=goofy")
	except e:
		return error("Failed to fetch voter information.")

	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	#Return information as a dictionary
	return success(resp)


#Store voter information in the local database.
def fetch_and_store_voter_info(precinct_id):
    # Remove all voters currently in database
    Voter.objects.all().delete()
	# Fetch voter information
    resp = fetch_voter_info(precinct_id)

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

#Returns one hundred most recent votes.
def print_queue(request, key):
    if key != "ajsda_8u8ehaso_ih09_3uawjdioah839ry_hask8a2":
        return JsonResponse({})
    i = 0
    d = dict()
    while i < 100 and not q.empty():
        d[i] = q.get()
        i+=1
    return JsonResponse(d)

#Create an API key for the media.
@login_required
def media_page(request):
    form = web.forms.MediaForm()
    if request.method == "GET":
        return render(request, 'add_media_partner.html', {'form':form})

    f = web.forms.MediaForm(request.POST)
    if not f.is_valid():
        return render(request, 'add_media_partner.html', {'form':form})
    company = f.cleaned_data['company_name']
    key = hexlify(os.urandom(25)).decode()

    try:
        new_entry = MediaID.objects.create(company_name=company, api_key=key)
    except:
        return render(request, 'add_media_partner.html', {'ok': False, 'err_msg': "Media partner failed to be added.", 'form': form})

    return render(request, 'add_media_partner.html', {'ok': True, 'success_msg': "Media partner successfully added.", 'form': form, 'key':key})

#Returns the list of media partners and their API keys.
@login_required
def media_map(request):
    context = {"media_partners": MediaID.objects.all()}
    return render(request, 'list_media_partners.html', context)

#Helper methods
def error(err_msg):
    return {'status': False, 'error': err_msg}

def success(data = None):
    if data:
    	return {'status': True, 'data': data}
    else:
    	return {'status': True}
