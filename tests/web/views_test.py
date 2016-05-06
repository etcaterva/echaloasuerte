import mock

from django.test import TestCase

from server.mongodb import driver
from web.views import pusher_authenticate


class TestPusher(TestCase):

    @mock.patch('web.views.pusher')
    def test_auth_with_post(self, pusher):
        req = mock.Mock()
        req.POST = {
            'channel_name': 'ch',
            'socket_id': 's1'
        }
        pusher.authenticate.return_value = {}
        pusher_authenticate(req)
        pusher.authenticate.assert_called_with(channel='ch', socket_id='s1')

    @mock.patch('web.views.pusher')
    def test_auth_with_body(self, pusher):
        req = mock.Mock()
        req.POST = {}
        req.body = "channel_name=ch&socket_id=s1"
        pusher.authenticate.return_value = {}
        pusher_authenticate(req)
        pusher.authenticate.assert_called_with(channel='ch', socket_id='s1')

