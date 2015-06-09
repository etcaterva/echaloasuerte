"""Common helpers for the pyhon code in the web project"""

from django.core.exceptions import PermissionDenied
from contextlib import contextmanager
from django.http import HttpRequest

import logging
import time


LOG = logging.getLogger("echaloasuerte")


def user_can_read_draw(user, draw, password=None):
    '''Validates that user can read draw. Throws unauth otherwise'''
    if not draw.user_can_read(user, password):
        LOG.info("User {0} not allowed to read draw {1}. Type: {2}, Password? {3}, Owner:{4}, Users: {5}"
                .format(user.pk, draw.pk, draw.shared_type, 'Y' if draw.password else 'N', draw.owner, draw.users))
        raise PermissionDenied()

def user_can_write_draw(user,draw):
    if not draw.user_can_write(user):
        LOG.info("User {0} not allowed to write draw {1}. Type: {2}, Password? {3}, Owner:{4}"
                .format(user.pk, draw.pk, draw.shared_type, 'Y' if draw.password else 'N', draw.owner))
        raise PermissionDenied()


@contextmanager
def _scoped_timer(func_name):
    st = time.time()
    yield
    elapsed = time.time() - st
    LOG.debug("{1} completed in {0:.2f}ms.".format(elapsed,func_name))

def _minimice(data):
    """Reduces the amount of info for some types of object"""
    if isinstance(data, HttpRequest):
        return dict(user=data.user.pk, post=data.POST, get=data.GET)
    else:
        return data

def time_it(func):
    """decorator to add trace information"""
    def _(*args,**kwargs):
        min_args = [_minimice(x) for x in args]
        min_kwargs = {k:_minimice(x) for k,x in kwargs.items()}
        LOG.debug("Calling: {0} with args: {1}, and kwargs {2}".format(func.__name__,min_args,min_kwargs))
        with _scoped_timer(func.__name__):
            return func(*args,**kwargs)
    return _
