from django.test import TestCase
import django

from server.bom.user import User
from server.bom import RandomNumberDraw
from server.mongodb.driver import MongoDriver


class TestServices(TestCase):
    """ Tests for the services """

    def setUp(self):
        django.setup()
        self._driver = MongoDriver.instance()


class TestToss(TestServices):
    """ Test the toss service
    """

    def setUp(self):
        super(TestToss, self).setUp()
        self.test_user = User("test_mail@yop.tu", password="fake_hashed_pwd")
        self.user_id = self._driver.save_user(self.test_user)
        self.test_draw = RandomNumberDraw(number_of_results=1)
        self._driver.save_draw(self.test_draw)
        self.req = lambda: None
        self.req.user = self.test_user

    def tearDown(self):
        self._driver._users.remove({"_id": self.user_id})
        self._driver._draws.remove({"_id": self.test_draw._id})

    def retrieve_draw(self):
        return self._driver.retrieve_draw(self.test_draw._id)


class TestAddUser(TestServices):
    """ Test the adding a user to a public draw
    """

    def setUp(self):
        super(TestAddUser, self).setUp()
        self.test_user = User("test_mail@yop.tu", password="fake_hashed_pwd")
        self.user_id = self._driver.save_user(self.test_user)
        self.test_draw = RandomNumberDraw(number_of_results=1, is_shared=True)
        self._driver.save_draw(self.test_draw)
        self.req = lambda: None
        self.req.user = self.test_user

    def tearDown(self):
        self._driver._users.remove({"_id": self.user_id})
        self._driver._draws.remove({"_id": self.test_draw._id})

    def retrieve_draw(self):
        return self._driver.retrieve_draw(self.test_draw._id)

