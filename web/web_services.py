"""definition of basic web services"""
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.core.validators import validate_email
from server import draw_factory
from server.mongodb.driver import MongoDriver
from web.common import user_can_read_draw, user_can_write_draw, time_it, invite_user, \
    set_owner, ga_track_draw
from server.forms import *
from server.bom import *
import dateutil.parser

LOG = logging.getLogger("echaloasuerte")
MONGO = MongoDriver.instance()


@login_required
@time_it
def update_user(request):
    """updates the details of a user"""
    # DEPRECATE
    user = MONGO.retrieve_user(request.user.pk)
    result = "ko"

    if "email" in request.POST:
        pass  # user._id = request.POST["email"]
    if "new_password" in request.POST:
        if "current_password" in request.POST and user.check_password(request.POST["current_password"]):
            user.set_password(request.POST["new_password"])
            result = "ok"
    if "alias" in request.POST:
        user.alias = request.POST["alias"]
        result = "ok"
    if "use_gravatar" in request.POST:
        user.use_gravatar= request.POST["use_gravatar"] == "true"
        result = "ok"
    MONGO.save_user(user)
    return HttpResponse(result)


@time_it
def feedback(request):
    """sends the feedback data to the users"""
    type_ = request.POST.get("type")
    comment = request.POST.get("comment")
    email = request.POST.get("email", "anonymous")
    browser = request.POST.get("browser", "Unknown Browser")
    subject = """Feedback ({0})""".format(type_)
    message = """{0}\nBy {1} on {2}""".format(comment,
                                              email,
                                              browser)
    if type_ and comment:
        mail_admins(subject, message, True)
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Invalid feedback, type or comment missing")

@login_required
@time_it
def add_favorite(request):
    """Add a draw to the list of favourites of an user"""
    # DEPRECATE
    draw_id = request.GET.get('draw_id')

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)  # raises 500
    user = MONGO.retrieve_user(request.user.pk)
    if draw_id in user.favourites:
        LOG.info("Draw {0} is favorite for user {1}".format(
            draw_id, request.user.pk))
        return HttpResponse()

    user.favourites.append(draw_id)
    MONGO.save_user(user)

    LOG.info("Draw {0} added as favorite for user {1}".format(
        draw_id, request.user.pk))
    return HttpResponse()


@login_required
@time_it
def remove_favorite(request):
    """removes a draw from the list of favourites"""
    # DEPRECATE
    draw_id = request.GET.get('draw_id')

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)  # raises 500
    user = MONGO.retrieve_user(request.user.pk)
    if draw_id not in user.favourites:
        LOG.info("Draw {0} is not favorite for user {1}".format(
            draw_id, request.user.pk))
        return HttpResponse()

    user.favourites.remove(draw_id)
    MONGO.save_user(user)

    LOG.info("Draw {0} removed as favorite for user {1}".format(
        draw_id, request.user.pk))
    return HttpResponse()


def check_access_to_draw(request):
    """Checks whether an user can access to a draw"""
    # is this used?
    draw_id = request.GET.get('draw_id')
    draw = MONGO.retrieve_draw(draw_id)

    user_can_read_draw(request.user, draw)
    return HttpResponse()


def add_message_to_chat(request):
    """Adds a message to a chat"""
    draw_id = request.GET.get('draw_id')
    message = request.GET.get('message')
    user = request.GET.get('user_name')
    MONGO.add_chat_message(draw_id, message, user)
    return HttpResponse()
