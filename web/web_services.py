"""definition of basic web services"""
import logging

from django.core.mail import mail_admins
from django.http import HttpResponseBadRequest, HttpResponse

from web.common import time_it


LOG = logging.getLogger("echaloasuerte")


@time_it
def feedback(request):
    """sends the feedback data to the users"""
    type_ = request.POST.get("type")
    comment = request.POST.get("comment")
    email = request.POST.get("email", "anonymous")
    browser = request.POST.get("browser", "Unknown Browser")
    subject = "Feedback ({0})".format(type_)
    message = u"{0}\nBy {1} on {2}".format(comment, email, browser)
    if type_ and comment:
        mail_admins(subject, message, True)
        return HttpResponse()
    else:
        return HttpResponseBadRequest(
            "Invalid feedback, type or comment missing")
