import datetime
import pytz

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

import django
from tastypie.test import ResourceTestCase

from server import bom, mongodb
from server.bom.card import CardDraw
from server.bom.coin import CoinDraw
from server.bom.dice import DiceDraw
from server.bom.link_sets import LinkSetsDraw
from server.bom.random_item import RandomItemDraw
from server.bom.random_letter import RandomLetterDraw
from server.bom.random_number import RandomNumberDraw
from server.bom.tournament import TournamentDraw


class DrawResource_ValidateTest(ResourceTestCase):
    urls = 'web.rest_api.urls'

    def setUp(self):
        super(DrawResource_ValidateTest, self).setUp()
        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        # base url of the resource
        self.base_url = '/v1/draw/'

        # Create an object we will use to test
        item = RandomNumberDraw()
        item.users = [self.user.pk]
        item.title = "Titulo"
        item.description = "A description, it can be long. Rather long"
        self.mongo.save_draw(item)
        self.item = item

        # We also build a detail URI, since we will be using it all over.
        self.detail_url = self.base_url + '{0}/'.format(
            urllib.quote(self.item.pk))

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)
        self.mongo.remove_draw(self.item.pk)

        # cleanup draws from other tests
        self.mongo._draws.remove({'owner': self.user.pk})

    def login(self):
        self.api_client.client.login(username='test@test.te',
                                     password='test')

    def invalid_title_test(self):
        data = {
            'title': 1,
            'is_shared': True,
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        self.assertHttpBadRequest(resp)

    def invalid_tournament_test(self):
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'type': 'tournament',
            'participants': "NOT A LIST"
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        self.assertHttpBadRequest(resp)

    def invalid_range_min_type_test(self):
        data = {
            'title': 'draw title',
            'is_shared': 'Yes',
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 'a',
            'range_max': 6,
            'allow_repeat': True,
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        self.assertHttpBadRequest(resp)


class DrawResourceTest(ResourceTestCase):
    urls = 'web.rest_api.urls'

    def setUp(self):
        super(DrawResourceTest, self).setUp()
        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        # base url of the resource
        self.base_url = '/v1/draw/'

        # Create an object we will use to test
        item = RandomNumberDraw()
        item.users = [self.user.pk]
        item.title = "Titulo"
        item.description = "A description, it can be long. Rather long"
        self.mongo.save_draw(item)
        self.item = item

        # We also build a detail URI, since we will be using it all over.
        self.detail_url = self.base_url + '{0}/'.format(
            urllib.quote(self.item.pk))

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)
        self.mongo.remove_draw(self.item.pk)

        # cleanup draws from other tests
        self.mongo._draws.remove({'users': self.user.pk})
        self.mongo._draws.remove({'owner': self.user.pk})

    def login(self):
        self.api_client.client.login(username='test@test.te',
                                     password='test')

    def test_anon_get_list_none(self):
        resp = self.api_client.get(self.base_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)

    def test_get_list_item(self):
        self.login()
        resp = self.api_client.get(self.base_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        # Here, we're checking an entire structure for the expected data.
        retrieved_draw = self.deserialize(resp)['objects'][0]
        self.assertEqual(retrieved_draw["is_shared"], self.item.is_shared)
        self.assertEqual(retrieved_draw["resource_uri"], self.detail_url)
        self.assertEqual(retrieved_draw["owner"], self.item.owner)
        self.assertEqual(retrieved_draw["title"], self.item.title)
        self.assertEqual(retrieved_draw["description"], self.item.description)
        self.assertEqual(retrieved_draw["users"], self.item.users)

    def test_anon_get_detail(self):
        resp = self.api_client.get(self.detail_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        # verify the keys, not all the data.
        for key in ['id', 'type', 'is_shared', 'owner', 'title',
                    'resource_uri', 'users', 'number_of_results']:
            self.assertTrue(key in self.deserialize(resp))

    def test_get_detail(self):
        self.login()
        resp = self.api_client.get(self.detail_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        # verify the keys, not all the data.
        for key in ['id', 'type', 'is_shared', 'owner', 'title',
                    'resource_uri', 'users', 'number_of_results']:
            self.assertTrue(key in self.deserialize(resp))

    def test_post_detail_bad_request(self):
        self.login()
        self.assertHttpBadRequest(self.api_client.post(self.base_url + "FAKE/",
                                                       format='json'))

    def test_post_detail_add_self(self):
        self.login()
        # Check how many are there first.
        self.item.users = ['FAKE@USER.es']
        self.mongo.save_draw(self.item)
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users,
                          ['FAKE@USER.es'])
        # create it
        self.assertHttpCreated(self.api_client.post(self.detail_url,
                                                    format='json'))

        # Verify a new one has been added.
        self.assertEquals(sorted(self.mongo.retrieve_draw(self.item.pk).users),
                         sorted(['FAKE@USER.es', self.user.pk]))

    def test_anon_delete_detail(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
                                                           format='json'))

    def test_anon_post_detail_remove_unauthorised(self):
        self.item.owner = self.user.pk
        self.mongo.save_draw(self.item)
        self.assertHttpUnauthorized(self.api_client.post(self.detail_url,
                                                    format='json',
                                                    data={
                                                        'remove_user': 'test@user.com'
                                                    }))

    def test_post_detail_anon_add_other(self):
        # Check how many are there first.
        self.item.owner = self.user.pk
        self.mongo.save_draw(self.item)
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users,
                          [self.user.pk])
        # create it
        self.assertHttpCreated(self.api_client.post(self.detail_url,
                                                    format='json',
                                                    data={
                                                        'add_user': ['FAKE@USER.es']
                                                    }))

        # Verify a new one has been added.
        self.assertEquals(sorted(self.mongo.retrieve_draw(self.item.pk).users),
                         sorted(['FAKE@USER.es', self.user.pk]))

    def test_post_detail_add_other(self):
        self.login()
        # Check how many are there first.
        self.mongo.save_draw(self.item)
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users,
                          [self.user.pk])
        # create it
        self.assertHttpCreated(self.api_client.post(self.detail_url,
                                                    format='json',
                                                    data={
                                                        'add_user': ['FAKE@USER.es']
                                                    }))
        self.assertEquals(sorted(self.mongo.retrieve_draw(self.item.pk).users),
                         sorted(['FAKE@USER.es', self.user.pk]))

    def test_post_detail_remove_other(self):
        self.login()
        # Check how many are there first.
        self.item.users.append('FAKE@USER.es')
        self.mongo.save_draw(self.item)
        self.assertEquals(sorted(self.mongo.retrieve_draw(self.item.pk).users),
                         sorted(['FAKE@USER.es', self.user.pk]))
        # remove it
        self.assertHttpCreated(self.api_client.post(self.detail_url,
                                                    format='json',
                                                    data={
                                                        'remove_user': 'FAKE@USER.es'
                                                    }))

        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users,
                          [self.user.pk])

    def test_delete_detail(self):
        self.login()
        # Check how many are there first.
        self.item.users = [self.user.pk]
        self.mongo.save_draw(self.item)
        self.assertIsNone(self.mongo.retrieve_draw(self.item.pk).owner)
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users,
                          [self.user.pk])
        # create it
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
                                                       format='json'))
        # Verify a new one has been added.
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users, [])
        self.assertIsNone(self.mongo.retrieve_draw(self.item.pk).owner)

    def test_owner_delete_detail(self):
        self.login()
        # Check how many are there first.
        self.item.owner = self.user.pk
        self.item.users = []
        self.mongo.save_draw(self.item)
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users, [])
        self.assertIsNotNone(self.mongo.retrieve_draw(self.item.pk).owner)
        # create it
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
                                                       format='json'))
        # Verify a new one has been added.
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users, [])
        self.assertIsNone(self.mongo.retrieve_draw(self.item.pk).owner)


class DrawResourceCreate_Test(ResourceTestCase):
    """Tests the creation of draws"""
    urls = 'web.rest_api.urls'

    def setUp(self):
        super(DrawResourceCreate_Test, self).setUp()
        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        # base url of the resource
        self.base_url = '/v1/draw/'

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)

        # cleanup draws
        self.mongo._draws.remove({'owner': self.user.pk})

    def login(self):
        self.api_client.client.login(username='test@test.te',
                                     password='test')

    def get_created_draw(self):
        """Retrieve a draw created by the user"""
        return self.mongo.get_draws_with_filter({'owner': self.user.pk})[0]

    def test_anon_create_random_number_ok(self):
        data = {
            'title': 'test_draw_with_no_owner',
            'is_shared': True,
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.mongo.get_draws_with_filter({
            'title': 'test_draw_with_no_owner'
        })[0]
        self.assertTrue(draw.is_feasible())

        self.assertIsNone(draw.owner)
        self.mongo.remove_draw(draw.pk)

    def test_create_shared_is_not_tossed(self):
        data = {
            'title': 'test_draw_with_no_owner',
            'is_shared': True,
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.mongo.get_draws_with_filter({
            'title': 'test_draw_with_no_owner'
        })[0]
        self.assertTrue(draw.is_feasible())

        self.assertEqual(len(draw.results), 0)
        self.mongo.remove_draw(draw.pk)

    def test_create_private_is_tossed(self):
        data = {
            'title': 'test_draw_with_no_owner',
            'is_shared': False,
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.mongo.get_draws_with_filter({
            'title': 'test_draw_with_no_owner'
        })[0]
        self.assertTrue(draw.is_feasible())

        self.assertEqual(len(draw.results), 1)
        self.mongo.remove_draw(draw.pk)

    def test_create_random_number_forbidden_att(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        for attr in ['results', 'owner', '_id', 'pk', 'creation_time',
                     'last_updated_time', 'audit']:
            data[attr] = "something"
            resp = self.api_client.post(self.base_url,
                                        format='json',
                                        data=data)
            self.assertHttpBadRequest(resp)
            data.pop(attr)
        self.assertEqual(0, len(self.mongo.get_draws_with_filter({
            'owner': self.user.pk})))

    def test_create_random_number_with_desc_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'description': 'The description',
            'is_shared': True,
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())
        self.assertEqual(draw.description,
                         data["description"])

    def test_create_random_number_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': [],
            'type': 'number',
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))

    def test_create_random_number_ok_2(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'type': 'number',
            'range_min': 0,
            'range_max': 2,
            'allow_repeat': False,
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is RandomNumberDraw)

    def test_create_random_bad_data_bad_request(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'type': 'number',
            'number_of_results': -1,
            'range_min': "2",
            'range_max': 2,
            'allow_repeat': False,
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpBadRequest(resp)

    def test_create_random_letter_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'type': 'letter',
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is RandomLetterDraw)

    def test_create_coin_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'number_of_results': 5,
            'users': ['ruben@prueba.com'],
            'type': 'coin',
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is CoinDraw)

    def test_create_dice_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'number_of_results': 5,
            'users': ['ruben@prueba.com'],
            'type': 'dice',
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is DiceDraw)

    def test_create_card_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'number_of_results': 5,
            'type_of_deck': 'french',
            'users': ['ruben@prueba.com'],
            'type': 'card',
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is CardDraw)

    def test_create_tournament_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'type': 'tournament',
            'participants': ["1", "2", "3", "4"]
            }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is TournamentDraw)

    def test_create_item_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'type': 'item',
            'items': ["1", "2", "3", "4"]
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is RandomItemDraw)

    def test_create_link_sets_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'type': 'link_sets',
            'sets': [["1", "2", "3", "4"],
                     ["a", "b", "c", "d"]]
        }
        resp = self.api_client.post(self.base_url,
                                    format='json',
                                    data=data)
        print(resp)
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))
        self.assertTrue(type(draw) is LinkSetsDraw)


class DrawResourceToss_Test(ResourceTestCase):
    """Tests the toss of draws"""
    # urls = 'web.rest_api.urls'

    def setUp(self):
        super(DrawResourceToss_Test, self).setUp()
        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        # base url of the resource
        self.base_url = '/api/v1/draw/'

    def schedule_toss(self, draw, schedule):
        toss_url = self.base_url + "{0}/schedule_toss/{1}/".format(draw.pk,
                                                                   schedule)
        return self.api_client.post(toss_url,
                                    format='json')

    def try_(self, data):
        toss_url = self.base_url + "try/"
        return self.api_client.post(toss_url,
                                    format='json',
                                    data=data)

    def toss(self, draw):
        toss_url = self.base_url + "{0}/toss/".format(draw.pk)
        return self.api_client.post(toss_url,
                                    format='json',
                                    data={})

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)

        # cleanup draws
        self.mongo._draws.remove({'owner': self.user.pk})

    def login(self):
        self.api_client.client.login(username='test@test.te',
                                     password='test')

    def test_toss_no_owner_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)

    def test_toss_not_owner_unauthorised(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = "random@user.si"
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpUnauthorized(resp)

    def test_toss_random_number_returns_result(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 5,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.assertEqual(5, self.deserialize(resp)['items'][0])
        self.mongo.remove_draw(draw.pk)

    def test_toss_random_number_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_toss_random_letter_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'allow_repeat': True,
            }
        draw = RandomLetterDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_toss_coin_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'allow_repeat': True,
            }
        draw = CoinDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_toss_dice_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'allow_repeat': True,
            }
        draw = DiceDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_toss_card_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'type_of_deck': 'french',
            'allow_repeat': True,
            }
        draw = CardDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_toss_tournament_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'participants': ["a", "b"],
            'allow_repeat': True,
            }
        draw = TournamentDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_toss_item_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'items': ["1"],
            'allow_repeat': True,
            }
        draw = RandomItemDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_toss_linked_sets_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'sets': [[1, 2], [2, 3]],
            'allow_repeat': True,
            }
        draw = LinkSetsDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.toss(draw)
        print(resp)
        self.assertHttpOK(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_try_bad_data_bad_request(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'type': 'link_sets',
            'users': ['ruben@prueba.com'],
            'sets': [[],
                     ["a", "b", "c", "d"]]
        }
        resp = self.try_(data)
        print(resp)
        self.assertHttpBadRequest(resp)

    def test_try_no_type_bad_request(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'users': ['ruben@prueba.com'],
            'sets': [["1", "2", "3", "4"],
                     ["a", "b", "c", "d"]]
        }
        resp = self.try_(data)
        print(resp)
        self.assertHttpBadRequest(resp)

    def test_try_invalid_type_bad_request(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': False,
            'enable_chat': False,
            'type': 'INVALID',
            'users': ['ruben@prueba.com'],
            'sets': [["1", "2", "3", "4"],
                     ["a", "b", "c", "d"]]
        }
        resp = self.try_(data)
        print(resp)
        self.assertHttpBadRequest(resp)

    def test_try_linked_sets_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'type': 'link_sets',
            'sets': [[1], [2]],
            'allow_repeat': True,
            }
        resp = self.try_(data)
        print(resp)
        self.assertHttpOK(resp)
        self.assertEqual([1, 2], self.deserialize(resp)['items'][0])

    def test_schedule_linked_sets_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'sets': [[1], [2]],
            'allow_repeat': True,
            }
        draw = LinkSetsDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.schedule_toss(draw, '2015-10-21T00:00:00Z')
        print(resp)
        self.assertHttpOK(resp)
        self.assertEqual([1, 2], self.deserialize(resp)['items'][0])
        self.assertEqual('2015-10-21T00:00:00',
                         self.deserialize(resp)['publication_datetime'])
        draw = self.mongo.retrieve_draw(draw.pk)
        self.assertEqual(1, len(draw.results))
        self.mongo.remove_draw(draw.pk)

    def test_schedule_empty_id_not_found(self):
        self.login()
        class FakeDraw(object):
            pk = ""
        resp = self.schedule_toss(FakeDraw(), '2015-10-21T00:00:00Z')
        print(resp)
        self.assertHttpNotFound(resp)


    def test_schedule_bad_id_not_found(self):
        self.login()
        class FakeDraw(object):
            pk = "INVALID_DRAW_ID"
        resp = self.schedule_toss(FakeDraw(), '2015-10-21T00:00:00Z')
        print(resp)
        self.assertHttpNotFound(resp)

    def test_schedule_linked_sets_missing_schedule(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'sets': [[1], [2]],
            'allow_repeat': True,
            }
        draw = LinkSetsDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.schedule_toss(draw, None)
        print(resp)
        self.assertHttpBadRequest(resp)
        self.mongo.remove_draw(draw.pk)

    def test_schedule_linked_sets_invalid_date(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'sets': [[1], [2]],
            'allow_repeat': True,
            }
        draw = LinkSetsDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        resp = self.schedule_toss(draw, 'invalid date :)')
        print(resp)
        self.assertHttpBadRequest(resp)
        self.mongo.remove_draw(draw.pk)


class DrawResourceUpdate_Test(ResourceTestCase):
    """Tests the update of draws"""
    # urls = 'web.rest_api.urls'

    def setUp(self):
        super(DrawResourceUpdate_Test, self).setUp()
        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        # base url of the resource
        self.base_url = '/api/v1/draw/'

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)

        # cleanup draws
        self.mongo._draws.remove({'owner': self.user.pk})

    def login(self):
        self.api_client.client.login(username='test@test.te',
                                     password='test')

    def detail_uri(self, draw):
        return self.base_url + draw.pk + '/'

    def test_update_no_owner_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        self.mongo.save_draw(draw)
        resp = self.api_client.patch(self.detail_uri(draw), data={})
        print(resp)
        self.assertHttpAccepted(resp)

    def test_update_not_owner_unauthorised(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = "random@user.si"
        self.mongo.save_draw(draw)
        resp = self.api_client.patch(self.detail_uri(draw), data={})
        print(resp)
        self.assertHttpUnauthorized(resp)

    def test_update_random_number_not_feasible(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'range_min': 70,
            'range_max': 60
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpBadRequest(resp)
        self.mongo.remove_draw(draw.pk)

    def test_update_random_number_fake_attributes(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        for attr in ['not_an_attribute', 'participants', 'a_test']:
            data[attr] = "something"
            resp = self.api_client.patch(self.detail_uri(draw),
                                         format='json',
                                         data=data)
            self.assertHttpAccepted(resp)
            updated_draw = self.mongo.retrieve_draw(draw.pk)
            self.assertFalse(hasattr(updated_draw, attr))
            data.pop(attr)
        self.mongo.remove_draw(draw.pk)

    def test_update_random_number_forbidden_att(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        for attr in ['results', 'owner', '_id', 'pk', 'creation_time',
                     'last_updated_time', 'audit']:
            data[attr] = "something"
            resp = self.api_client.patch(self.detail_uri(draw),
                                         format='json',
                                         data=data)
            self.assertHttpBadRequest(resp)
            data.pop(attr)
        self.mongo.remove_draw(draw.pk)

    def test_update_random_number_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'range_min': 5,
            'range_max': 6,
            'allow_repeat': True,
            }
        draw = RandomNumberDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'range_min': 50,
            'range_max': 60
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)

    def test_update_random_letter_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'allow_repeat': True,
            }
        draw = RandomLetterDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'users': ["test1@u.o", "test2@l.o"]
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)

    def test_update_coin_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'allow_repeat': True,
            }
        draw = CoinDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'users': []
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)

    def test_update_dice_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'allow_repeat': True,
            }
        draw = DiceDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'number_of_results': 5
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)

    def test_update_card_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'type_of_deck': 'french',
            'allow_repeat': True,
            }
        draw = CardDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'type_of_deck': 'french'
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)

    def test_update_tournament_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'participants': ["a", "b"],
            }
        draw = TournamentDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'participants': ['Javier', 'Ruben', 'Josemari'],
            'enable_chat': False
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)

    def test_update_item_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'items': ["1"],
            'allow_repeat': True,
            }
        draw = RandomItemDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'items': [1, 2, 3, 4],
            'title': 'new title'
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)

    def test_update_linked_sets_ok(self):
        self.login()
        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'sets': [[1, 2], [2, 3]],
            'allow_repeat': True,
            }
        draw = LinkSetsDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        update_data = {
            'sets': [
                ["One", "Two", "Three"],
                ["Caramba", "Jeropa"]
            ]
        }
        resp = self.api_client.patch(self.detail_uri(draw), data=update_data)
        print(resp)
        self.assertHttpAccepted(resp)
        draw = self.mongo.retrieve_draw(draw.pk)
        for key, value in update_data.items():
            self.assertEqual(value, getattr(draw, key))
        self.mongo.remove_draw(draw.pk)


class DrawResourceChat_Test(ResourceTestCase):
    """Tests the update of draws"""
    # urls = 'web.rest_api.urls'

    def setUp(self):
        super(DrawResourceChat_Test, self).setUp()
        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        data = {
            'title': 'test_draw',
            'is_shared': True,
            'enable_chat': True,
            'users': ['user_anon@user.es'],
            'sets': [[1, 2], [2, 3]],
            'allow_repeat': True,
            }
        draw = LinkSetsDraw(**data)
        draw.owner = self.user.pk
        self.mongo.save_draw(draw)
        self.draw = draw

        # base url of the resource
        self.base_url = '/api/v1/draw/'

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)

        self.mongo.remove_draw(self.draw.pk)

    def login(self):
        self.api_client.client.login(username='test@test.te',
                                     password='test')

    def detail_uri(self, draw):
        return self.base_url + draw.pk + '/'

    def chat_uri(self, draw):
        return self.detail_uri(draw) + 'chat/'

    def test_get_empty_chat_draw(self):
        self.login()
        draw = self.draw
        resp = self.api_client.get(self.chat_uri(draw))
        print(resp)
        self.assertHttpOK(resp)
        self.assertEqual(0,
                         len(self.deserialize(resp)["messages"]))

    def test_get_chat_draw(self):
        self.login()
        draw = self.draw
        self.mongo.add_chat_message(draw.pk,
                                    "chat message",
                                    "anon")
        resp = self.api_client.get(self.chat_uri(draw))
        print(resp)
        self.assertHttpOK(resp)
        self.assertEqual(1,
                         len(self.deserialize(resp)["messages"]))
        self.assertEqual("chat message",
                         self.deserialize(resp)["messages"][0]["content"])

    def test_get_user_chat_draw(self):
        self.login()
        draw = self.draw
        self.mongo.add_chat_message(draw.pk,
                                    "chat message",
                                    self.user.pk)
        resp = self.api_client.get(self.chat_uri(draw))
        print(resp)
        self.assertHttpOK(resp)
        self.assertEqual(1,
                         len(self.deserialize(resp)["messages"]))
        self.assertEqual(self.user.pk,
                         self.deserialize(resp)["messages"][0]["user"])

    def test_get_no_user_chat_draw(self):
        self.login()
        draw = self.draw
        self.mongo.add_chat_message(draw.pk,
                                    "chat message",
                                    "anon")
        resp = self.api_client.get(self.chat_uri(draw))
        print(resp)
        self.assertHttpOK(resp)
        self.assertEqual(1,
                         len(self.deserialize(resp)["messages"]))
        self.assertEqual("anon",
                         self.deserialize(resp)["messages"][0]["user"])

    def test_anon_post_chat(self):
        draw = self.draw
        resp = self.api_client.post(self.chat_uri(draw), data={
            "message": "chat message",
            "anonymous_alias": "anon user"
        })
        print(resp)
        self.assertHttpOK(resp)
        chats = self.mongo.retrieve_chat_messages(draw.pk)
        self.assertEqual(1, len(chats))
        self.assertEqual(None, chats[0]["user"])
        self.assertEqual("anon user", chats[0]["anonymous_alias"])

    def test_auth_with_alias_post_chat(self):
        self.login()
        draw = self.draw
        resp = self.api_client.post(self.chat_uri(draw), data={
            "user": self.user.pk,
            "message": "chat message",
            "anonymous_alias": "anon user"
        })
        print(resp)
        self.assertHttpOK(resp)
        chats = self.mongo.retrieve_chat_messages(draw.pk)
        self.assertEqual(1, len(chats))
        self.assertEqual(self.user.pk, chats[0]["user"])
        self.assertRaises(Exception, lambda: chats[0]["anonymous_alias"])

    def test_post_chat(self):
        self.login()
        draw = self.draw
        resp = self.api_client.post(self.chat_uri(draw), data={
            "message": "chat message",
            "user": self.user.pk
        })
        print(resp)
        self.assertHttpOK(resp)
        chats = self.mongo.retrieve_chat_messages(draw.pk)
        self.assertEqual(1, len(chats))
        self.assertEqual(self.user.pk, chats[0]["user"])
        self.assertEqual("chat message", chats[0]["content"])
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self.assertTrue(now > chats[0]["creation_time"])
        self.assertTrue(now - datetime.timedelta(minutes=5) <
                        chats[0]["creation_time"])

    def test_post_on_existing_chat(self):
        self.login()
        draw = self.draw
        self.mongo.add_chat_message(draw.pk,
                                    "chat message",
                                    "anon")
        resp = self.api_client.post(self.chat_uri(draw), data={
            "message": "chat message",
            "user": self.user.pk
        })
        print(resp)
        self.assertHttpOK(resp)
        chats = self.mongo.retrieve_chat_messages(draw.pk)
        self.assertEqual(2, len(chats))
        self.assertEqual(self.user.pk, chats[0]["user"])
        self.assertEqual("anon", chats[1]["user"])

    def test_post_missing_data(self):
        draw = self.draw
        resp = self.api_client.post(self.chat_uri(draw), data={
            "user": self.user.pk
        })
        print(resp)
        self.assertHttpBadRequest(resp)

        resp = self.api_client.post(self.chat_uri(draw), data={
            "message": "chat message",
        })
        print(resp)
        self.assertHttpBadRequest(resp)
