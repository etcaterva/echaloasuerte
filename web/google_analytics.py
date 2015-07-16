import logging
from django.utils.http import urlencode
from django.conf import settings
try:
    from httplib import HTTPConnection
except ImportError:
    from http.client import HTTPConnection
import http.client

LOG = logging.getLogger("echaloasuerte")

def ga_track_event(category, action, label=None, value=None):
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    if not ga_prop_id:
        return
    if not action or not category:
        LOG.warning("Error sending event to Google Analytics (Category={0}, Action={1})".format(category, action))
        return

    params_dict = {
        'v': 1,
        'tid': settings.GOOGLE_ANALYTICS_PROPERTY_ID,
        'cid': '666',
        't': 'event',
        'ec': category,
        'ea': action,
        'ev': 0
    }
    if label:
        params_dict['el'] = label
    if value:
        params_dict['ev'] = value


    params = urlencode(params_dict)
    connection = http.client.HTTPConnection('www.google-analytics.com')
    connection.request('POST', '/collect', params)