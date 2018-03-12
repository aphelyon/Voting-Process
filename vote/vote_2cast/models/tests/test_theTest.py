from django.test import TestCase


class SampleTest(TestCase):
	def test_theTester(self):
		self.assertEqual(1+1, 2)
	