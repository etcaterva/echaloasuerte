"""Common helpers for the pyhon code in the web project"""

from django.core.exceptions import PermissionDenied
from django.contrib.staticfiles.templatetags.staticfiles import static
from contextlib import contextmanager
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

import logging
import time
from web.google_analytics import ga_track_event


LOG = logging.getLogger("echaloasuerte")

INVITE_EMAIL_TEMPLATE = _("""ChooseRandom.com
You have been invited to a shared draw
--------------------------------------
{user} has invited you to his shared draw "{title}"

Join now at https://chooserandom.com/draw/{draw_id}

Good Luck!
The Choose Random Team
""")
INVITE_HTML_EMAIL_TEMPLATE = _("""
<img src="https://chooserandom.com/{image_url}" alt="Choose Random">
<h2>You have been invited to a shared draw</h2>
<p>{user} has invited you to his shared draw "{title}"</p>
<a href="https://chooserandom.com/draw/{draw_id}"><h3>Join Now</h3></a>
<p>Good Luck!<br />
The Choose Random Team</p>
""")


def invite_user(users_email, draw)
    owner = draw.owner.alias if draw.owner else _("An anonymous user")
    draw_id = draw.pk
    draw_title = draw.title if draw.title or _("Draw without a title")
    LOG.info("Inviting users {0} to draw {1}".format(users_email, draw_id))
    arguments = {
        "image_url": static("brand_en.png"),
        "user": owner,
        "title": draw_title
        "draw_id": draw_id
    }
    try:
        send_mail('Choose Random',
                  INVITE_EMAIL_TEMPLATE.format(**arguments),
                  'draws@chooserandom.com',
                  users_email,
                  html_message=INVITE_HTML_EMAIL_TEMPLATE.format(**arguments))
    except Exception as error:
        LOG.error("Unexpected error when inviting user {0}: {1}".format(users_email,
                                                                        error))


def user_can_read_draw(user, draw):
    """Validates that user can read draw. Throws unauth otherwise"""
    if not draw.check_read_access(user):
        LOG.info("User {0} not allowed to read draw {1}. Shared: {2}, Owner:{3}, Users: {4}"
                 .format(user.pk, draw.pk, draw.is_shared, draw.owner, draw.users))
        raise PermissionDenied("Unauthorised to read the draw")


def user_can_write_draw(user, draw):
    if not draw.check_write_access(user):
        LOG.info("User {0} not allowed to write draw {1}. Shared: {2}, Owner:{3}"
                 .format(user.pk, draw.pk, draw.is_shared, draw.owner))
        raise PermissionDenied("Unauthorised to write the draw")


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


def ga_track_draw(bom_draw, action):
    """Sends a notification of action to google analytics

    :bom_draw: draw to send information about
    :action: action to send
    """
    shared_type = 'public' if bom_draw.is_shared else 'private'
    ga_track_event(category=action, action=bom_draw.draw_type, label=shared_type)


def set_owner(draw, request):
    """Best effort to set the owner given a request"""
    try:
        draw.owner = request.user.pk
    except:
        pass
