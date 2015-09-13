import urllib

import django
from tastypie.test import ResourceTestCase

from server import bom, mongodb
from server.bom.random_number import RandomNumberDraw


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

    def test_anon_post_detail(self):
        self.assertHttpUnauthorized(self.api_client.post(self.detail_url,
                                                         format='json',
                                                         data={}))

    def test_post_detail_bad_request(self):
        self.login()
        self.assertHttpBadRequest(self.api_client.post(self.base_url + "FAKE/",
                                                       format='json'))

    def test_post_detail(self):
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
        self.assertEquals(self.mongo.retrieve_draw(self.item.pk).users,
                          ['FAKE@USER.es', self.user.pk])

    def test_anon_patch_detail(self):
        self.assertHttpMethodNotAllowed(self.api_client.patch(self.detail_url,
                                                              format='json',
                                                              data={}))

    def test_patch_detail(self):
        self.login()
        self.assertHttpMethodNotAllowed(self.api_client.patch(self.detail_url,
                                                              format='json',
                                                              data={}))

    def test_anon_delete_detail(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
                                                           format='json'))

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
        print resp
        self.assertHttpCreated(resp)
        draw = self.mongo.get_draws_with_filter({
            'title': 'test_draw_with_no_owner'
        })[0]
        self.assertTrue(draw.is_feasible())

        self.assertIsNone(draw.owner)
        self.mongo.remove_draw(draw.pk)

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
        print resp
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
        print resp
        self.assertHttpCreated(resp)
        draw = self.get_created_draw()
        self.assertTrue(draw.is_feasible())

        data.pop('type')
        for key, value in data.items():
            self.assertEqual(value, getattr(draw, key))

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
        for attr in []:
            data["attr"] = "something"
            resp = self.api_client.post(self.base_url,
                                        format='json',
                                        data=data)
            self.assertHttpBadRequest(resp)
            data.pop(attr)
        self.assertEqual(0, len(self.mongo.get_draws_with_filter({
            'owner': self.user.pk})))

