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

def add_message_to_chat(request):
    """Adds a message to a chat"""
    draw_id = request.GET.get('draw_id')
    message = request.GET.get('message')
    user = request.GET.get('user_name')
    MONGO.add_chat_message(draw_id, message, user)
    return HttpResponse()
