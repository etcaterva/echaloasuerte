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
    data = {}
    if request.method == 'POST':
        draw_form = RandomNumberDrawForm(request.POST)
        if draw_form.is_valid():
            draw = draw_form.save()
            if draw.is_feasible():
                result = draw.toss()
                list = []
                for number in result.numbers.all():
                    list.append(number.value)
                data = {'results': list}
            else:
                print "The draw is not feasible!"
        else:
            print draw_form.errors
    else:
        draw_form = RandomNumberDrawForm()

    data['draw'] = draw_form
    return render_to_response('random_number.html', data, context_instance=RequestContext(request))