try:
    import urllib.parse as urllib
except ImportError:
    import urllib

import django
from tastypie.test import ResourceTestCase

from server import bom, mongodb


class UserResourceTest(ResourceTestCase):
    urls = 'web.rest_api.urls'

    def setUp(self):
        super(UserResourceTest, self).setUp()

        django.setup()

        # mongodb instance
        self.mongo = mongodb.MongoDriver.instance()

        # Create a user for authentication
        test_user = bom.User('test@test.te')
        test_user.set_password('test')
        self.mongo.save_user(test_user)
        self.user = test_user

        # base url of the resource
        self.base_url = '/v1/user/'

        # Create an object we will use to test
        item = self.user
        item.alias = 'The alias'
        self.mongo.save_user(item)
        self.item = item

        # We also build a detail URI, since we will be using it all over.
        self.detail_url = self.base_url + '{0}/'.format(
            urllib.quote(self.item.pk))

        # The data we'll send on POST requests.
        self.post_data = {
            'email': 'testemail@email.com',
            'alias': 'user_alias',
            'password': 'secret_password'
        }

    def tearDown(self):
        self.api_client.client.logout()
        self.mongo.remove_user(self.user.pk)
        self.mongo.remove_user(self.item.pk)
        self.mongo.remove_user(self.post_data["email"])

    def login(self):
        self.api_client.client.login(username='test@test.te',
                                     password='test')

    def test_logout(self):
        self.login()
        login_url = self.base_url + 'logout/'
        resp = self.api_client.post(login_url, format='json')
        self.assertHttpOK(resp)

    def test_login_ok(self):
        credentials = {
            "email": "test@test.te",
            "password": "test"
        }
        login_url = self.base_url + 'login/'
        resp = self.api_client.post(login_url, format='json', data=credentials)
        self.assertHttpOK(resp)

    def test_login_wrong_email(self):
        credentials = {
            "email": "non_existing@test.te",
            "password": "test"
        }
        login_url = self.base_url + 'login/'
        resp = self.api_client.post(login_url, format='json', data=credentials)
        self.assertHttpUnauthorized(resp)

    def test_login_wrong_password(self):
        credentials = {
            "email": "test@test.te",
            "password": "wrong_password"
        }
        login_url = self.base_url + 'login/'
        resp = self.api_client.post(login_url, format='json', data=credentials)
        self.assertHttpUnauthorized(resp)

    def test_anon_get_list_none(self):
        resp = self.api_client.get(self.base_url, format='json')
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)

    def test_get_list_self(self):
        self.login()
        resp = self.api_client.get(self.base_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        # Here, we're checking an entire structure for the expected data.
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'alias': self.item.alias,
            'email': self.item.email,
            'resource_uri': self.detail_url,
            'use_gravatar': self.item.use_gravatar
        })

    def test_anon_get_detail(self):
        resp = self.api_client.get(self.detail_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        # We use ``assertKeys`` here to just verify the keys, not all the data.
        self.assertKeys(self.deserialize(resp),
                        ['email', 'alias', 'resource_uri', 'use_gravatar'])
        self.assertEqual(self.deserialize(resp)['email'], self.item.email)

    def test_get_detail(self):
        self.login()
        resp = self.api_client.get(self.detail_url,
                                   format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(self.deserialize(resp), {
            'alias': self.item.alias,
            'email': self.item.email,
            'resource_uri': self.detail_url,
            'use_gravatar': self.item.use_gravatar
        })

    def test_anon_post_list(self):
        self.assertRaises(mongodb.MongoDriver.NotFoundError,
                          lambda: self.mongo.retrieve_user(
                              self.post_data['email']))
        count_users = self.mongo._users.count()
        self.assertHttpCreated(self.api_client.post(self.base_url,
                                                    format='json',
                                                    data=self.post_data))
        # Verify a new one has been added.
        self.assertIsNotNone(self.mongo.retrieve_user(self.post_data['email']))
        self.assertEqual(self.mongo._users.count(), count_users + 1)

    def test_post_list(self):
        self.assertRaises(mongodb.MongoDriver.NotFoundError,
                          lambda: self.mongo.retrieve_user(
                              self.post_data['email']))
        self.login()
        # Check how many are there first.
        count_users = self.mongo._users.count()
        self.assertHttpCreated(self.api_client.post(self.base_url,
                                                    format='json',
                                                    data=self.post_data))
        # Verify a new one has been added.
        self.assertIsNotNone(self.mongo.retrieve_user(self.post_data['email']))
        self.assertEqual(self.mongo._users.count(), count_users + 1)

    def test_anon_patch_detail(self):
        self.assertHttpUnauthorized(self.api_client.patch(self.detail_url,
                                                          format='json',
                                                          data={}))

    def test_patch_detail(self):
        self.login()
        new_data = {'alias': 'new_alias'}

        count_users = self.mongo._users.count()
        self.assertHttpAccepted(self.api_client.patch(self.detail_url,
                                                      format='json',
                                                      data=new_data))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(self.mongo._users.count(), count_users)
        # check unchanged data
        self.assertEqual(self.mongo.retrieve_user(self.item.pk).email,
            self.item.email)
        self.assertEqual(self.mongo.retrieve_user(self.item.pk).use_gravatar,
                         self.item.use_gravatar)
        # Check for updated data.
        self.assertEqual(self.mongo.retrieve_user(self.item.pk).alias,
                         'new_alias')

    def test_patch_bad_request(self):
        self.login()
        for attr in ['email']:
            new_data = {attr: 'new_data'}
        self.assertHttpBadRequest(self.api_client.patch(self.detail_url,
                                                        format='json',
                                                        data=new_data))

    def test_anon_delete_detail(self):
        self.assertHttpMethodNotAllowed(self.api_client.delete(self.detail_url,
                                                               format='json'))

    def test_delete_detail(self):
        self.assertHttpMethodNotAllowed(self.api_client.delete(self.detail_url,
                                                               format='json'))
