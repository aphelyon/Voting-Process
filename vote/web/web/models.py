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


class AnonVote(models.Model):
    uniqueID = models.IntegerField()
    voted = models.CharField(max_length=75)
    voting_status = models.BooleanField()

class BallotEntry(models.Model):
    num_votes = models.IntegerField()
    party = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    election_id = models.CharField(max_length=100)
    candidate_id = models.IntegerField()
    def as_json(self):
        return dict(party=self.party, position=self.position, num_votes=self.num_votes, candidate_id=self.candidate_id, election_id=self.election_id)

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ballotEntries = models.ManyToManyField(BallotEntry)
    dob = models.DateField()
    def as_json(self):
        return dict(first_name=self.first_name, last_name=self.last_name, dob=self.dob, pk=self.pk)

class Election(models.Model):
    election_id = models.CharField(max_length=100, primary_key=True)
    election_type = models.CharField(max_length=100)
    ballotEntries = models.ManyToManyField(BallotEntry)
    def as_json(self):
        return dict(election_id=self.election_id, election_type=self.election_type, pk=self.pk)