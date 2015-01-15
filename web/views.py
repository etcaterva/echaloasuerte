from django.http import *
from server.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.translation import ugettext_lazy as _
from server.bom.random_item import RandomItemDraw
from server.bom.random_number import RandomNumberDraw
from server.bom.coin import CoinDraw
from server.bom.dice import DiceDraw
from server.bom.card import CardDraw
from server.bom.user import User
from server.mongodb.driver import MongoDriver
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


logger = logging.getLogger("echaloasuerte")
mongodb = MongoDriver.instance()

def set_owner(draw,request):
    """Best effort to set the owner given a request"""
    try:
        draw.owner = request.user._id
    except:
        pass

def login_user(request):
    logger.info("Serving login_user")
    logout(request)
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            context = {'error': "Username or password not valid."}
    return render(request, 'login.html', context)


def register(request):
    logger.info("Serving register page")
    logout(request)
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        u = User(username)
        u.set_password(password)
        try:
            mongodb.create_user(u)
            return login_user(request)
        except Exception as e:
            context = {'error': _("Username is already taken.")}
    return render(request, 'register.html', context)


@login_required
def profile(request):
    logger.info("Serving profile page for user {0}".format(request.user))
    try:
        draws = mongodb.get_user_draws(request.user._id)
    except Exception as e:
        logger.error("There was an issue when retrieving user draws. {0}".format(draws))

    context = {'draws': draws}
    return render(request, 'profile.html', context)


def index(request):
    logger.info("Serving index page.")
    return render(request, 'index.html')


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
            set_owner(bom_draw,request)
            if bom_draw.is_feasible():
                result = bom_draw.toss()
                mongodb.save_draw(bom_draw)
                res_numbers = result["items"]
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
            set_owner(bom_draw,request)
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
    logger.info("Serving view for coin draw")
    context = {}
    context['errors'] = []
    if request.method == 'POST':
        logger.debug("Information posted. {0}".format(request.POST))
        bom_draw = CoinDraw()
        set_owner(bom_draw,request)
        result = bom_draw.toss()
        mongodb.save_draw(bom_draw)
        res = result["items"][0]
        context['result'] = res
        logger.info("New result generated for draw {0}".format(bom_draw._id))
        logger.debug("Generated draw: {0}".format(bom_draw))
    return render(request, 'coin.html', context)


def dice_draw(request):
    logger.info("Serving view for dice draw")
    context = {}
    context['errors'] = []

    if request.method == 'POST':
        draw_form = DiceDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            bom_draw = DiceDraw(**raw_draw)
            set_owner(bom_draw,request)
            if bom_draw.is_feasible():
                result = bom_draw.toss()
                mongodb.save_draw(bom_draw)
                res = result["items"]
                context['results'] =  res
                logger.info("New result generated for draw {0}".format(bom_draw._id))
                logger.debug("Generated draw: {0}".format(bom_draw))
            else:
                logger.info("Draw not feasible")
                context['errors'].append(_("The draw is not feasible"))
        else:
            logger.info("Form not valid")
            logger.debug("Errors in the form: {0}".format(draw_form.errors))
    else:
        draw_form = DiceDrawForm()

    context['draw'] = draw_form
    return render(request, 'dice.html', context)


def card_draw(request):
    logger.info("Serving view for card draw")
    context = {}
    context['errors'] = []

    if request.method == 'POST':
        draw_form = CardDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            bom_draw = CardDraw(**raw_draw)
            set_owner(bom_draw,request)
            if bom_draw.is_feasible():
                result = bom_draw.toss()
                mongodb.save_draw(bom_draw)
                res = result["items"]
                context['results'] =  res
                logger.info("New result generated for draw {0}".format(bom_draw._id))
                logger.debug("Generated draw: {0}".format(bom_draw))
            else:
                logger.info("Draw not feasible")
                context['errors'].append(_("The draw is not feasible"))
        else:
            logger.info("Form not valid")
            logger.debug("Errors in the form: {0}".format(draw_form.errors))
    else:
        draw_form = CardDrawForm()

    context['draw'] = draw_form
    return render(request, 'card.html', context)


def under_construction(request):
    return render(request, 'under_construction.html', {})
