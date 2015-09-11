import urllib
import django
from tastypie.test import ResourceTestCase

from server import bom, mongodb
from server.bom.random_number import RandomNumberDraw


class FavouriteResourceTest(ResourceTestCase):
    urls = 'web.rest_api.urls'

    def setUp(self):
        super(FavouriteResourceTest, self).setUp()

        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        # base url of the resource
        self.base_url = '/v1/favourite/'

        # Create an object we will use to test
        item = RandomNumberDraw()
        self.mongo.save_draw(item)
        self.user.favourites.append(item.pk)
        self.mongo.save_user(self.user)
        self.item = item

        # We also build a detail URI, since we will be using it all over.
        self.detail_url = self.base_url + '{0}/'.format(
            urllib.quote(self.item.pk))

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)
        self.mongo.remove_draw(self.item.pk)

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
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'id': self.item.pk,
            'type': self.item.draw_type,
            'resource_uri': self.detail_url
        })

    def test_anon_get_detail(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.detail_url,
                                                            format='json'))

    def test_get_detail(self):
        self.login()
        self.assertHttpMethodNotAllowed(self.api_client.get(self.detail_url,
                                                            format='json'))

    def test_anon_post_list(self):
        self.assertHttpUnauthorized(self.api_client.post(self.base_url,
                                                         format='json'))

    def test_post_list(self):
        self.login()
        # Check how many are there first.
        self.user.favourites.remove(self.item.pk)
        self.mongo.save_user(self.user)
        self.assertEqual(self.mongo.retrieve_user(self.user.pk).favourites, [])
        # create it
        self.assertHttpCreated(self.api_client.post(self.base_url,
                                                    format='json',
                                                    data={'id': self.item.pk}))
        # Verify a new one has been added.
        self.assertEqual(self.mongo.retrieve_user(self.user.pk).favourites,
                         [self.item.pk])

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
        self.assertEqual(self.mongo.retrieve_user(self.user.pk).favourites,
                         [self.item.pk])
        # create it
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
                                                       format='json'))
        # Verify a new one has been added.
        self.assertEqual(self.mongo.retrieve_user(self.user.pk).favourites, [])

