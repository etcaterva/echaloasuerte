from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger("echaloasuerte")

# Create your views here.
def index(request):
    logger.info("Serving index page.")
    return render_to_response('index.html', {'request':request},
        context_instance=RequestContext(request))
