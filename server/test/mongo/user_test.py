from django.test import TestCase
from server.bom.user import *
from server.mongodb.driver import *
import django


class SanityMongo(TestCase):
    """ Basic sanity test for mongodb driver"""
    def setUp(self):
        django.setup()
        self._driver = MongoDriver.instance()

    def persist_user_test(self):
        """MongoDB: Persist and retrieve user"""
        tested_item = User("myemail@yop.tu", password="fake_hashed_pwd")
        res_id = self._driver.save_user(tested_item)
        raw = self._driver._users.find_one({"_id":res_id})
        for k,v in tested_item.__dict__.items():
            self.assertTrue(k in raw.keys())
            self.assertTrue(v == raw[k])
        self._driver._users.remove({"_id":res_id})

    def retrieve_users_test(self):
        """MongoDB: Retrieves an item using mongodb driver"""
        tested_item = User("myemail@yop.tu", password="fake_hashed_pwd")
        res_id = self._driver.save_user(tested_item)
        retrieved = self._driver.retrieve_user(res_id)

        self.assertIsInstance(retrieved,User)
        for k,v in tested_item.__dict__.items():
            self.assertTrue(k in retrieved.__dict__.keys())
            self.assertEqual(v , retrieved.__dict__[k])
        self._driver._users.remove({"_id":res_id})

    def retrieve_users_mail_test(self):
        """MongoDB: Retrieves an item using mongodb driver by email"""
        self._driver._users.remove({"email":"myemail@yop.tu"})
        tested_item = User("myemail@yop.tu", password="fake_hashed_pwd")
        res_id = self._driver.save_user(tested_item)
        retrieved = self._driver.retrieve_user("myemail@yop.tu")

        self.assertIsInstance(retrieved,User)
        for k,v in tested_item.__dict__.items():
            self.assertTrue(k in retrieved.__dict__.keys())
            self.assertEqual(v , retrieved.__dict__[k])
        self._driver._users.remove({"_id":res_id})
