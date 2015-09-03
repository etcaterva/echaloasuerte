from django.test import TestCase
from server.bom.random_number import *
from server.bom.user import User
from django.contrib.auth.models import AnonymousUser


class WritePermissionWithLoggedUserTest(TestCase):
    """ Tests to check bom permissioning system when we have a logged in user"""

    def setUp(self):
        self.draw = RandomNumberDraw()
        self.user = User("test")

    def user_is_owner_test(self):
        self.draw.owner = self.user.pk
        self.assertTrue(self.draw.user_can_write(self.user))

    def draw_with_no_owner_test(self):
        self.draw.owner = None
        self.assertTrue(self.draw.user_can_write(self.user))

    def draw_with_another_owner_test(self):
        self.draw.owner = User("another guy")
        self.assertFalse(self.draw.user_can_write(self.user))


class WritePermissionWithNotLoggedUserTest(TestCase):
    """ Tests to check bom permissioning system when we have a not logged user"""

    def setUp(self):
        self.draw = RandomNumberDraw()
        self.user = AnonymousUser()

    def draw_with_no_owner_test(self):
        self.draw.owner = None
        self.assertTrue(self.draw.user_can_write(self.user))

    def draw_with_another_owner_test(self):
        self.draw.owner = User("another guy")
        self.assertFalse(self.draw.user_can_write(self.user))


class ReadPermissionWithLoggedUserPublicTest(TestCase):
    def setUp(self):
        self.draw = RandomNumberDraw(shared_type='Public')
        self.user = User("test")

    def user_is_owner_test(self):
        self.draw.owner = self.user.pk
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_no_owner_test(self):
        self.draw.owner = None
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_another_owner_test_empty_user_list(self):
        self.draw.owner = User("another guy")
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append(self.user.pk)
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_not_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append("anotherguy")
        self.assertTrue(self.draw.user_can_read(self.user))


class ReadPermissionWithNotLoggedUserPublicTest(TestCase):
    def setUp(self):
        self.draw = RandomNumberDraw(shared_type='Public')
        self.user = AnonymousUser()

    def draw_with_no_owner_test(self):
        self.draw.owner = None
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_another_owner_test_empty_user_list(self):
        self.draw.owner = User("another guy")
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_not_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append("anotherguy")
        self.assertTrue(self.draw.user_can_read(self.user))


class ReadPermissionWithLoggedUserInviteTest(TestCase):
    def setUp(self):
        self.draw = RandomNumberDraw(shared_type='Invite')
        self.user = User("test")

    def user_is_owner_test(self):
        self.draw.owner = self.user.pk
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_no_owner_test(self):
        self.draw.owner = None
        self.assertFalse(self.draw.user_can_read(self.user))

    def draw_with_another_owner_test_empty_user_list(self):
        self.draw.owner = User("another guy")
        self.assertFalse(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append(self.user.pk)
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_not_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append("anotherguy")
        self.assertFalse(self.draw.user_can_read(self.user))


class ReadPermissionWithNotLoggedUserInviteTest(TestCase):
    def setUp(self):
        self.draw = RandomNumberDraw(shared_type='Invite',)
        self.user = AnonymousUser()

    def draw_with_no_owner_test(self):
        self.draw.owner = None
        self.assertFalse(self.draw.user_can_read(self.user))

    def draw_with_another_owner_test_empty_user_list(self):
        self.draw.owner = User("another guy")
        self.assertFalse(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_not_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append("anotherguy")
        self.assertFalse(self.draw.user_can_read(self.user))

class ReadPermissionWithLoggedUserNoneTest(TestCase):
    def setUp(self):
        self.draw = RandomNumberDraw(shared_type='None')
        self.user = User("test")

    def user_is_owner_test(self):
        self.draw.owner = self.user.pk
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_no_owner_test(self):
        self.draw.owner = None
        self.assertTrue(self.draw.user_can_read(self.user))

    def draw_with_another_owner_test_empty_user_list(self):
        self.draw.owner = User("another guy")
        self.assertFalse(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append(self.user.pk)
        self.assertFalse(self.draw.user_can_read(self.user))

    def draw_with_another_owner_user_not_in_list_test(self):
        self.draw.owner = User("another guy")
        self.draw.users.append("anotherguy")
        self.assertFalse(self.draw.user_can_read(self.user))
