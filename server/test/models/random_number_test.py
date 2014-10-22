from django.test import TestCase
from server.models import *
# Create your tests here.
class RandonNumberTestCase(TestCase):
    def setUp(self):
        pass

    def build_random_number_test(self):
        """Builds a random number pool"""
        tested_item = RandomNumberPoll()

    def poll_default_constructor_test(self):
        """Validate a randon number just constructed sets the default values"""
        tested_item = RandomNumberPoll()
        self.assertEqual(tested_item.range_min,0)
        self.assertEqual(tested_item.range_max,None)
        self.assertEqual(tested_item.number_of_results,1)
        self.assertEqual(tested_item.allow_repeat,False)

    def poll_parametrized_constructor_test(self):
        """Test parametrized constructor for RandonNumberPoll"""
        tested_item = RandomNumberPoll(range_max = 5,allow_repeat=True, number_of_results = 1)
        self.assertEqual(tested_item.range_min,0)
        self.assertEqual(tested_item.range_max,5)
        self.assertEqual(tested_item.number_of_results,1)
        self.assertEqual(tested_item.allow_repeat,True)

    def is_feasible_default_test(self):
        """Default RandonNumberPoll is not feasible"""
        self.assertFalse(RandomNumberPoll().is_feasible())

    def is_feasible_simple_test(self):
        """Simple RandonNumberPoll is feasible"""
        tested_item = RandomNumberPoll(range_max=5)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_limit_ok_test(self):
        """Border case for RandonNumberPoll is feasible OK"""
        tested_item = RandomNumberPoll(range_max=5,range_min=2,number_of_results=3,allow_repeat=False)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_limit_ko_test(self):
        """Border case for RandonNumberPoll is feasible KO"""
        tested_item = RandomNumberPoll(range_max=5,range_min=2,number_of_results=4,allow_repeat=False)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_limit_ko_with_repeat(self):
        """Border case for RandonNumberPoll is feasible with repeat"""
        tested_item = RandomNumberPoll(range_max=5,range_min=2,number_of_results=4,allow_repeat=True)
        self.assertTrue(tested_item.is_feasible())

    def draw_poll_relationship_after_save_test(self):
        """Validates the relation ship from draw to poll"""
        t_poll = RandomNumberPoll(range_max=10)
        t_poll.save()
        t_draw1 = RandomNumberDraw(value=10)
        t_draw2 = RandomNumberDraw(value=10)
        self.assertEqual(0, t_poll.draws.count())
        t_draw1.poll = t_poll
        self.assertEqual(0, t_poll.draws.count())
        t_draw1.save()
        self.assertEqual(1, t_poll.draws.count())
        t_draw2.poll = t_poll
        t_draw2.save()
        self.assertEqual(2, t_poll.draws.count())
