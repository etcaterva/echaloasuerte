from django.test import TestCase
from server.models import *
import django


class RandomItemDrawTestCase(TestCase):
    def setUp(self):
        django.setup()

    def build_random_item_from_list_test(self):
        """RandomItemDraw: Basic construction"""
        RandomItemDraw()

    def default_constructor_test(self):
        """RandomItemDraw: Default constructor"""
        tested_item = RandomItemDraw()
        self.assertEqual(tested_item.number_of_results, 1)
        self.assertEqual(tested_item.allow_repeat, False)

    def parametrized_constructor_test(self):
        """RandomItemDraw: Full Parametrized constructor"""
        tested_item = RandomItemDraw(number_of_results=5, allow_repeat=True)
        self.assertEqual(tested_item.number_of_results, 5)
        self.assertEqual(tested_item.allow_repeat, True)

    def is_feasible_default_test(self):
        """RandomItemDraw: Default constructor is not feasible"""
        t_draw = RandomItemDraw()
        t_draw.save()
        self.assertFalse(t_draw.is_feasible())

    def is_feasible_simple_test(self):
        """RandomItemDraw: Simple parametrized constructor is feasible"""
        t_draw = RandomItemDraw()
        t_draw.save()
        t_item = Item(name="item1")
        t_item.save()
        t_draw.items.add(t_item)
        self.assertTrue(t_draw.is_feasible())

    def is_feasible_too_many_results_without_repeat_test(self):
        """RandomItemDraw: Too many results without repeat is not feasible"""
        number_of_results = 3
        t_draw = RandomItemDraw(number_of_results=number_of_results, allow_repeat=False)
        t_item1 = Item(name="table")
        t_item2 = Item(name="pencil")
        t_draw.save()
        t_item1.save()
        t_item2.save()
        t_draw.items.add(t_item1, t_item2)

        self.assertFalse(t_draw.is_feasible())

    def relationship_draw_result_test(self):
        """RandomNumberDraw: Relationship Draw-Result"""
        t_draw = RandomItemDraw()
        t_draw.save()
        t_result1 = RandomItemResult()
        t_result1.draw = t_draw
        t_result2 = RandomItemResult()
        t_result2.draw = t_draw
        self.assertEqual(0, t_draw.results.count())
        t_result1.save()
        self.assertEqual(1, t_draw.results.count())
        t_result2.save()
        self.assertEqual(2, t_draw.results.count())

    def relationship_result_item_test(self):
        """RandomItemDraw: Relationship Result-Item"""
        t_draw = RandomItemDraw()
        t_draw.save()
        t_result = RandomItemResult()
        t_result.draw = t_draw
        t_result.save()

        t_item1 = Item(name="pencil")
        t_item1.save()
        t_item2 = Item(name="table")
        t_item2.save()
        self.assertEqual(0, t_result.items.all().count())
        result1 = RandomItemResultItem(result=t_result, item=t_item1)
        result1.save()

        self.assertEqual(1, t_result.items.all().count())
        result2 = RandomItemResultItem(result=t_result, item=t_item2)
        result2.save()
        self.assertEqual(2, t_result.items.all().count())

    def toss_one_result_test(self):
        """RandomItemDraw: Each toss generates a new result"""
        t_draw = RandomItemDraw()
        t_item1 = Item(name="table")
        t_item2 = Item(name="pencil")
        t_draw.save()
        t_item1.save()
        t_item2.save()

        t_draw.items.add(t_item1, t_item2)
        self.assertEqual(0, t_draw.results.count())
        t_draw.toss()
        self.assertEqual(1, t_draw.results.count())
        t_draw.toss()
        self.assertEqual(2, t_draw.results.count())

    def toss_result_contains_items_test(self):
        """RandomItemDraw: after a toss items are in results"""
        number_of_results = 2
        t_draw = RandomItemDraw(number_of_results=number_of_results)
        t_item1 = Item(name="table")
        t_item2 = Item(name="pencil")
        t_item3 = Item(name="notebook")
        t_item4 = Item(name="bottle")
        t_draw.save()
        t_item1.save()
        t_item2.save()
        t_item3.save()
        t_item4.save()

        t_draw.items.add(t_item1, t_item2, t_item3, t_item4)
        t_draw.toss()
        result = t_draw.results.latest('timestamp')
        counter = 0
        counter += result.items.filter(id=t_item1.id).count()
        counter += result.items.filter(id=t_item2.id).count()
        counter += result.items.filter(id=t_item3.id).count()
        counter += result.items.filter(id=t_item4.id).count()
        self.assertEqual(number_of_results, counter)


    def toss_without_repeat_test(self):
        """RandomNumberDraw: Unique results if allow_repeat is false"""
        t_draw = RandomItemDraw(number_of_results=9, allow_repeat=False)
        t_draw.save()
        item1 = Item(name="item1")
        item2 = Item(name="item2")
        item3 = Item(name="item3")
        item4 = Item(name="item4")
        item5 = Item(name="item5")
        item6 = Item(name="item6")
        item7 = Item(name="item7")
        item8 = Item(name="item8")
        item9 = Item(name="item9")
        item1.save()
        item2.save()
        item3.save()
        item4.save()
        item5.save()
        item6.save()
        item7.save()
        item8.save()
        item9.save()

        t_draw.items.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
        t_draw.toss()
        result = t_draw.results.latest('timestamp')
        self.assertEqual(1, result.items.filter(id=item1.id).count())
        self.assertEqual(1, result.items.filter(id=item2.id).count())
        self.assertEqual(1, result.items.filter(id=item3.id).count())
        self.assertEqual(1, result.items.filter(id=item4.id).count())
        self.assertEqual(1, result.items.filter(id=item1.id).count())
        self.assertEqual(1, result.items.filter(id=item5.id).count())
        self.assertEqual(1, result.items.filter(id=item6.id).count())
        self.assertEqual(1, result.items.filter(id=item7.id).count())
        self.assertEqual(1, result.items.filter(id=item8.id).count())
        self.assertEqual(1, result.items.filter(id=item9.id).count())

