from django.db import models


class Voter(models.Model):
	voter_number = models.CharField(max_length = 20)
	voter_status = models.CharField(max_length = 20)
	date_registered = models.CharField(max_length = 20)
	last_name = models.CharField(max_length = 50)
	first_name = models.CharField(max_length = 50)
	street_address = models.CharField(max_length = 75)
	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 15)
	zipcode = models.CharField(max_length = 20)
	locality = models.CharField(max_length = 50)
	precinct = models.CharField(max_length = 50)
	precinct_id = models.CharField(max_length = 20)