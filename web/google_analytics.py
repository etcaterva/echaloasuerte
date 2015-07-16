import logging
from django.utils.http import urlencode
import http.client
from django.conf import settings

LOG = logging.getLogger("echaloasuerte")

def ga_track_event(category, action, label=None, value=None):
    if not settings.GOOGLE_ANALYTICS_PROPERTY_ID:
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