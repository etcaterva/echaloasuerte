from django.test import TestCase
from server.models import RandomNumberPoll
# Create your tests here.
class RandonNumberPollTestCase(TestCase):
    def setUp(self):
	pass

    def build_random_number(self):
        """Builds a random number pool"""
	tested_item = RandomNumberPoll()
	

