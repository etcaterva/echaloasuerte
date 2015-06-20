from django.test import TestCase
from server.bom.random_number import *
from server.bom.user import *
from server.mongodb.driver import *
import django


class SanityMongo(TestCase):
    """ Basic sanity test for mongodb driver"""
    def setUp(self):
        django.setup()
        self._driver = MongoDriver.instance()

    def persist_draw_test(self):
        """MongoDB: Persist and retrieve RandomNumberDraw"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        res_id = self._driver.save_draw(tested_item)
        raw = self._driver._draws.find_one({"_id":res_id})
        for k,v in tested_item.__dict__.items():
            if k in ("creation_time","last_updated_time"):
                continue
            self.assertTrue(k in raw.keys())
            self.assertTrue(v == raw[k])
        self._driver._draws.remove({"_id":res_id})

    def raw_retrieve_test(self):
        """MongoDB: Persist and retrieve RandomNumberDraw"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        res_id = self._driver.save_draw(tested_item)
        draw = RandomNumberDraw(**self._driver._draws.find_one({"_id":res_id}))

        for k,v in tested_item.__dict__.items():
            if k in ("creation_time","last_updated_time"):
                continue
            self.assertTrue(k in draw.__dict__.keys())
            self.assertEqual(v , draw.__dict__[k])
        self._driver._draws.remove({"_id":res_id})

    def retrieve_draw_test(self):
        """MongoDB: Retrieves an item using mongodb driver"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        res_id = self._driver.save_draw(tested_item)
        retrieved = self._driver.retrieve_draw(res_id)

        self.assertIsInstance(retrieved,RandomNumberDraw)
        for k,v in tested_item.__dict__.items():
            self.assertTrue(k in retrieved.__dict__.keys())
            self.assertTrue(v == retrieved.__dict__[k])
        self._driver._draws.remove({"_id":res_id})

    def retrieve_draw_test(self):
        """MongoDB: Retrieves an item using mongodb driver smart method"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        res_id = self._driver.save_draw(tested_item)
        retrieved = self._driver.retrieve_draw(res_id)
        self.assertEqual(type(retrieved),RandomNumberDraw)

    def retrieve_draw_withowner_test(self):
        """MongoDB: Saves and retrieve a draw wich has an owner"""
        u = User("test@email.com")
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        tested_item.owner = u._id
        res_id = self._driver.save_draw(tested_item)
        retrieved = self._driver.retrieve_draw(res_id)
        self.assertEqual(retrieved.owner, u._id)
        res = self._driver.get_user_draws(u._id)
        self.assertTrue(len([x for x in res["owner"] if x._id == res_id ]) > 0)
        self._driver._draws.remove({"_id":res_id})

