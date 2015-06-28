"""Common helpers for the pyhon code in the web project"""

from django.core.exceptions import PermissionDenied
from contextlib import contextmanager
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

import logging
import time


LOG = logging.getLogger("echaloasuerte")

INVITE_EMAIL_TEMPLATE = _("""
Hi!

You have been invited to a draw in echaloasuerte by {0}
Your link is http://www.echaloasuerte.com/draw/{1}/ .

Good Luck,
Echaloasuerte.com Team
""")


def invite_user(user_email, draw_id, owner_user):
    LOG.info("Inviting user {0} to draw {1}".format(user_email, draw_id))
    send_mail('Echaloasuerte', INVITE_EMAIL_TEMPLATE.format(owner_user, draw_id),
              'draws@echaloasuerte.com', user_email, fail_silently=True)


def user_can_read_draw(user, draw, password=None):
    '''Validates that user can read draw. Throws unauth otherwise'''
    if not draw.user_can_read(user, password):
        LOG.info("User {0} not allowed to read draw {1}. Type: {2}, Password? {3}, Owner:{4}, Users: {5}"
                 .format(user.pk, draw.pk, draw.shared_type, 'Y' if draw.password else 'N', draw.owner, draw.users))
        raise PermissionDenied()


def user_can_write_draw(user, draw):
    if not draw.user_can_write(user):
        LOG.info("User {0} not allowed to write draw {1}. Type: {2}, Password? {3}, Owner:{4}"
                 .format(user.pk, draw.pk, draw.shared_type, 'Y' if draw.password else 'N', draw.owner))
        raise PermissionDenied()


@contextmanager
def _scoped_timer(func_name):
    st = time.time()
    yield
    elapsed = time.time() - st
    LOG.debug("{1} completed in {0:.2f}ms.".format(elapsed, func_name))


def _minimice(data):
    """Reduces the amount of info for some types of object"""
    if isinstance(data, HttpRequest):
        return dict(user=data.user.pk, post=data.POST, get=data.GET)
    else:
        return data


def time_it(func):
    """decorator to add trace information"""

    def _(*args, **kwargs):
        min_args = [_minimice(x) for x in args]
        min_kwargs = {k: _minimice(x) for k, x in kwargs.items()}
        LOG.debug("Calling: {0} with args: {1}, and kwargs {2}".format(func.__name__, min_args, min_kwargs))
        with _scoped_timer(func.__name__):
            return func(*args, **kwargs)

    return _
