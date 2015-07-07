# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import pytz
import datetime
from django import template
from django.template import defaultfilters
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware, utc
from django.utils.translation import ugettext, ungettext_lazy

register = template.Library()

@register.filter
def is_future(value):
    """
    Given a datetime check if it is future
    If the datetime has no tz, utc is assumed
    """
    if not isinstance(value, datetime.datetime):
        raise RuntimeError("Invalid type, datetime required")

    if value.tzinfo is None:
        value = value.replace(tzinfo=pytz.utc)
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    return value > now
