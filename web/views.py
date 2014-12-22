from server.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.translation import ugettext_lazy as _
import logging
from server.bom.random_item import RandomItemDraw
from server.bom.random_number import RandomNumberDraw
from server.mongodb.driver import MongoDriver


logger = logging.getLogger("echaloasuerte")
mongodb = MongoDriver.instance()


# Create your views here.
def index(request):
    logger.info("Serving index page.")
    return render_to_response('index.html', {'request': request}, context_instance=RequestContext(request))


def random_number_draw(request):
    logger.info("Serving view for random number draw")
    context = {}
    context['errors'] = []
    if request.method == 'POST':
        logger.debug("Information posted. {0}".format(request.POST))
        draw_form = RandomNumberDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            #in the future we could retrive draws, add results and list the historic
            bom_draw = RandomNumberDraw(**raw_draw)#This works because form and python object have the same member names
            if bom_draw.is_feasible():
                result = bom_draw.toss()
                mongodb.save_draw(bom_draw)
                res_numbers = result["numbers"]
                context['results'] =  res_numbers
                logger.info("New result generated for draw {0}".format(bom_draw._id))
                logger.debug("Generated draw: {0}".format(bom_draw))
            else:
                logger.info("Draw not feasible")
                context['errors'].append(_("The draw is not feasible"))
        else:
            logger.info("Form not valid")
            logger.debug("Errors in the form: {0}".format(draw_form.errors))
    else:
        draw_form = RandomNumberDrawForm()

    context['draw'] = draw_form
    return render(request, 'random_number.html', context)


def random_item_draw(request):
    logger.info("Serving view for random number draw")
    context = {}
    context['errors'] = []

    if request.method == 'POST':
        draw_form = RandomItemDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            raw_draw["items"] = raw_draw["items"].split(',')
            bom_draw = RandomItemDraw(**raw_draw)
            if bom_draw.is_feasible():
                result = bom_draw.toss()
                mongodb.save_draw(bom_draw)
                res_items = result["items"]
                context['results'] =  res_items
                logger.info("New result generated for draw {0}".format(bom_draw._id))
                logger.debug("Generated draw: {0}".format(bom_draw))
            else:
                logger.info("Draw not feasible")
                context['errors'].append(_("The draw is not feasible"))
        else:
            logger.info("Form not valid")
            logger.debug("Errors in the form: {0}".format(draw_form.errors))
    else:
        draw_form = RandomItemDrawForm()

    context['draw'] = draw_form
    return render(request, 'random_item.html', context)


def coin_draw(request):
    context = {}
    if request.method == 'POST':
        draw_form = CoinDrawForm(request.POST)
        if draw_form.is_valid():
            draw = draw_form.save()
            if draw.is_feasible():
                result = draw.toss()
                context = {'result': result.value}
            else:
                print("The draw is not feasible!")
        else:
            print(draw_form.errors)
    else:
        draw_form = CoinDrawForm()

    context['draw'] = draw_form
    return render(request, 'coin.html', context)


def dice_draw(request):
    context = {}
    if request.method == 'POST':
        draw_form = DiceDrawForm(request.POST)
        if draw_form.is_valid():
            draw = draw_form.save()
            if draw.is_feasible():
                result = draw.toss()
                list = []
                for number in result.dice.all():
                    list.append(number.value)
                context = {'results': list}
            else:
                print("The draw is not feasible!")
        else:
            print(draw_form.errors)
    else:
        draw_form = DiceDrawForm()

    context['draw'] = draw_form
    return render(request, 'dice.html', context)

def under_construction(request):
    return render(request, 'under_construction.html', {})
