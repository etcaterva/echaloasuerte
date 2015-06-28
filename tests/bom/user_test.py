from django.test import TestCase
from server.bom.user import *


class UserTest(TestCase):
    def setUp(self):
        self.dummy_user = User("a@a.a")

    def default_constructor_test(self):
        """User: Basic construction"""
        pass

    def check_password_empty_test(self):
        self.assertFalse(self.dummy_user.check_password("23"))

    def check_password_ko_test(self):
        self.dummy_user.set_password("123")
        self.assertFalse(self.dummy_user.check_password("23"))

    def check_password_ok_test(self):
        self.dummy_user.set_password("123")
        self.assertTrue(self.dummy_user.check_password("123"))

    def get_username_id_is_email_test(self):
        self.assertEqual("mario", User("mario@weirdmail.com").get_username())

    def get_username_id_is_not_email_test(self):
        self.assertEqual("marioX", User("marioX").get_username())

    def get_email_test(self):
        self.assertEqual("mario@gmail.com", User("mario@gmail.com").get_email())
