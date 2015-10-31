from django.test import TestCase
import django
from django.core.exceptions import PermissionDenied

from server.bom.user import User
from server.bom import RandomNumberDraw
from server.mongodb.driver import MongoDriver
from web.web_services import add_favorite, remove_favorite


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


class TestFavourites(TestServices):
    """ Test the adding/removing favourites
    """

    def setUp(self):
        super(TestFavourites, self).setUp()
        self.test_user = User("test_mail@yop.tu", password="fake_hashed_pwd")
        self.user_id = self._driver.save_user(self.test_user)
        self.test_draw = RandomNumberDraw(number_of_results=1)
        self._driver.save_draw(self.test_draw)
        self.req = lambda: None
        self.req.user = self.test_user

    def tearDown(self):
        self._driver._users.remove({"_id": self.user_id})
        self._driver._draws.remove({"_id": self.test_draw._id})

    def retrieve_user(self):
        return self._driver.retrieve_user(self.test_user._id)

    def add_favourite_test(self):
        self.assertEqual(
            0,
            len(self.retrieve_user().favourites)
        )
        self.req.GET = {"draw_id": self.test_draw._id}
        add_favorite(self.req)
        self.assertEqual(
            1,
            len(self.retrieve_user().favourites)
        )

    def add_not_owner_test(self):
        self.assertEqual(
            0,
            len(self.retrieve_user().favourites)
        )
        self.test_draw.owner = "FAKE"
        self._driver.save_draw(self.test_draw)
        self.req.GET = {"draw_id": self.test_draw._id}
        self.assertRaises(
            PermissionDenied,
            lambda: add_favorite(self.req)
        )

    def add_wrong_drawn_test(self):
        self.assertEqual(
            0,
            len(self.retrieve_user().favourites)
        )
        self.req.GET = {"draw_id": "FAKE"}
        self.assertRaises(
            Exception,
            lambda: add_favorite(self.req)
        )

    def add_remove_favourite_test(self):
        self.assertEqual(
            0,
            len(self.retrieve_user().favourites)
        )
        self.req.GET = {"draw_id": self.test_draw._id}
        add_favorite(self.req)
        remove_favorite(self.req)
        self.assertEqual(
            0,
            len(self.retrieve_user().favourites)
        )

    def remove_non_favourite_test(self):
        self.assertEqual(
            0,
            len(self.retrieve_user().favourites)
        )
        self.req.GET = {"draw_id": self.test_draw._id}
        remove_favorite(self.req)
        self.assertEqual(
            0,
            len(self.retrieve_user().favourites)
        )
