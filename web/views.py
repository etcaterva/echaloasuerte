from server.forms import *

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


def random_number_draw(request):
    if request.method == 'POST':
        form = RandomNumberDrawForm(request.POST)
        if form.is_valid():
            draw = form.save()
            if draw.is_feasible():
                draw.toss()
                return index(request)
            else:
                print "The draw is not feasible!"
        else:
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = RandomNumberDrawForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('random_number.html', {'form':form}, context_instance=RequestContext(request))