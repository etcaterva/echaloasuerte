from django.test import TestCase
import django
from django.core.exceptions import PermissionDenied

from server.bom.user import User
from server.bom import RandomNumberDraw
from server.mongodb.driver import MongoDriver
from web.web_services import update_user, add_favorite, remove_favorite


class TestServices(TestCase):
    """ Tests for the services """

    def setUp(self):
        django.setup()
        self._driver = MongoDriver.instance()


class TestUpdateUserProfile(TestServices):
    """ Test the update user service
    """

    def setUp(self):
        super(TestUpdateUserProfile, self).setUp()
        self.tested_user = User("test_mail@yop.tu")
        self.tested_user.set_password("fake_pwd")
        self.user_id = self._driver.save_user(self.tested_user)
        self.req = lambda: None
        self.req.user = self.tested_user

    def tearDown(self):
        self._driver._users.remove({"_id": self.user_id})

    def update_email_test(self):
        """Test updating the email of an user"""
        self.req.POST = {"email": "new_email@y.x"}
        update_user(self.req)
        self.assertEqual(
            "test_mail@yop.tu",
            # "new_email@y.x",
            self._driver.retrieve_user(self.tested_user._id).pk
        )

    def update_password_ok_test(self):
        """Test updating the password of an user"""
        self.req.POST = {"current_password": "fake_pwd",
                         "new_password": "new_awesome_password"}
        update_user(self.req)
        self.assertTrue(
            self._driver.retrieve_user(self.tested_user._id).check_password(
                "new_awesome_password"
            )
        )

    def update_password_ko_test(self):
        """Test updating the password of an user"""
        self.req.POST = {"current_password": "wrong_pwd",
                         "new_password": "new_awesome_password"}
        update_user(self.req)
        self.assertFalse(
            self._driver.retrieve_user(self.tested_user._id).check_password(
                "new_awesome_password"
            )
        )

    def update_alias_test(self):
        """Test updating the alias of an user"""
        self.req.POST = {"alias": "the_coolest_alias"}
        update_user(self.req)
        self.assertEqual(
            "the_coolest_alias",
            self._driver.retrieve_user(self.tested_user._id).alias
        )

    def update_avatar_test(self):
        """Test updating the avatar of an user"""
        self.req.POST = {"use_gravatar" : "true"}
        update_user(self.req)
        self.assertEqual(
            True,
            self._driver.retrieve_user(self.tested_user._id).use_gravatar
        )


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
