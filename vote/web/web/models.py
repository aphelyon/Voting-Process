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


class Election(models.Model):
    election_id = models.CharField(max_length=100, primary_key=True)
    election_type = models.CharField(max_length=100)
    def as_json(self):
        return dict(election_id = self.election_id, election_type=self.election_type)

class Position(models.Model):
    positionName = models.CharField(max_length=100)

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    num_votes = models.IntegerField()
    party = models.CharField(max_length=100)
    dob = models.DateField()
    elections = models.ManyToManyField(Election)
    positions = models.ManyToManyField(Position)
    def as_json(self):
        return dict(first_name = self.first_name, last_name=self.last_name, num_votes=self.num_votes, party=self.party, dob=self.dob, pk=self.pk)
