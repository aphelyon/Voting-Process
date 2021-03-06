from django.db import models


class Voter(models.Model):
    voter_number = models.CharField(max_length=20)
    voter_status = models.CharField(max_length=20)
    date_registered = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=75)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=20)
    locality = models.CharField(max_length=50)
    precinct = models.CharField(max_length=50)
    precinct_id = models.CharField(max_length=20)
    def as_json(self):
        return dict(first_name = self.first_name, last_name=self.last_name, street_address=self.street_address, voter_status=self.voter_status)

class BallotEntry(models.Model):
    party = models.CharField(max_length=100)
    position = models.CharField(max_length=100000)
    num_votes = models.IntegerField()
    candidate_id = models.IntegerField()
    election_id = models.CharField(max_length=100)
    precinct_id = models.CharField(max_length=15)
    def as_json(self):
        return dict(party=self.party, position=self.position, num_votes=self.num_votes, pk=self.pk, candidate_id=self.candidate_id, election_id=self.election_id, precinct_id=self.precinct_id)

class AnonVote(models.Model):
    hash = models.CharField(max_length=100)
    ballotEntries = models.ManyToManyField(BallotEntry)
    def as_json(self):
        return dict(pk=self.hash)

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    ballotEntries = models.ManyToManyField(BallotEntry)
    def as_json(self):
        return dict(first_name = self.first_name, last_name=self.last_name, dob=self.dob, pk=self.pk)

class Election(models.Model):
    election_id = models.CharField(max_length=100, primary_key=True)
    election_type = models.CharField(max_length=100)
    ballotEntries = models.ManyToManyField(BallotEntry)
    def as_json(self):
        return dict(election_id = self.election_id, election_type=self.election_type, pk=self.pk)

class MediaID(models.Model):
    api_key = models.CharField(max_length = 100, primary_key = True)
    company_name = models.CharField(max_length = 100)
    def as_json(self):
        return dict(company = company_name, key = api_key)
