from django.test import TestCase
from server.mongodb.driver import *
import django


class SanityMongo(TestCase):
    """ Basic sanity test for mongodb driver"""
    def setUp(self):
        django.setup()
        self._driver = MongoDriver()
        self.dummy_doc = {"test-id":"SINGLE TEST ID"}

    def connection_test(self):
        """MongoDB: Basic construction"""
        pass

    def can_write_users_test(self):
        """MongoDB: Raw insert in users collection"""
        self._driver._users.insert(self.dummy_doc)
        self._driver._users.remove(self.dummy_doc)

    def can_write_draws_test(self):
        """MongoDB: Raw insert in draws collection"""
        self._driver._draws.insert(self.dummy_doc)
        self._driver._draws.remove(self.dummy_doc)


    def can_read_draws_test(self):
        """MongoDB: Raw read in draws collection"""
        self._driver._draws.insert(self.dummy_doc)
        self._driver._draws.find(self.dummy_doc)[0]
        self._driver._users.remove(self.dummy_doc)

    def can_read_users_test(self):
        """MongoDB: Raw read in users collection"""
        self._driver._users.insert(self.dummy_doc)
        self._driver._users.find(self.dummy_doc)[0]
        self._driver._draws.remove(self.dummy_doc)
