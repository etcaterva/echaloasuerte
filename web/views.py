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
from server.bom.link_sets import LinkSetsDraw
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


def find_previous_version(curr_draw):
    """
    Search in the DB for a previous draw with the same id. If found, the old and current version are compared.
    If the draw configuration didn't change returns the old version so later the results will be added to this one
    Otherwise it will clean the draw id (so mongo will assign a new one to it later). A link to the older version of the
    draw is added.
    """
    if curr_draw.pk == '':
        curr_draw._id = None
        return curr_draw
    prev_draw = mongodb.retrieve_draw(curr_draw.pk)
    for k, v in curr_draw.__dict__.items():
        if k not in ["creation_time", "results", "_id"] and (k not in prev_draw.__dict__.keys() or v != prev_draw.__dict__[k]):
            # Data have changed
            logger.info("Draw with id {0} changed on key {1}".format(prev_draw._id,k))
            curr_draw.prev_draw = prev_draw._id
            # Clean the current's draw id, so a new one will be assigned to it
            curr_draw._id = None
            return curr_draw
    # Data haven't changed so return previous draw to work on it
    return prev_draw


def user_can_read_draw(user,draw):
    return user._id == draw.owner

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
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            context = {'error': "Email or password not valid."}
    return render(request, 'login.html', context)


def register(request):
    logger.info("Serving register page")
    logout(request)
    context = {}
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        u = User(email)
        u.set_password(password)
        try:
            mongodb.create_user(u)
            return login_user(request)
        except Exception as e:
            context = {'error': _("The email is already registered.")}
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


def random_number_draw(request,draw_id = None):
    logger.info("Serving view for random number draw")
    context = {'errors': []}

    if request.method == 'POST':
        logger.debug("Information posted. {0}".format(request.POST))
        draw_form = RandomNumberDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            #in the future we could retrive draws, add results and list the historic
            bom_draw = RandomNumberDraw(**raw_draw)#This works because form and python object have the same member names
            set_owner(bom_draw, request)

            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                result = bom_draw.toss()
                mongodb.save_draw(bom_draw)

                # TODO Option 1
                draw_form.data = draw_form.data.copy()
                draw_form.data['_id'] = bom_draw.pk

                # TODO Option 2
                #draw_form = RandomNumberDrawForm(initial=bom_draw.__dict__)

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
        if draw_id:
            requested_draw = mongodb.retrieve_draw(draw_id)
            logger.debug("Filling form with retrieved draw {0}".format(requested_draw))
            draw_form = RandomNumberDrawForm(initial=requested_draw.__dict__)
        else:
            draw_form = RandomNumberDrawForm()

    context['draw'] = draw_form
    return render(request, 'random_number.html', context)


def retrieve_draw(request,draw_id):
    logger.info("Serving view for retrieve draw with id {0}".format(draw_id))
    context = {}
    context['errors'] = []
    bom_draw = mongodb.retrieve_draw(draw_id)
    if bom_draw:
        if user_can_read_draw(request.user,bom_draw):
            context['draw'] = bom_draw
        else:
            context['errors'].append("Draw not found") #Even if not authorised we return not found. Security
            logger.info("User {0} is not authoriced to read draw {1}".format(request.user._id,bom_draw._id))
    else:
        context['errors'].append("Draw not found")
        logger.info("Draw with id {0} not found.".format(draw_id))

    return render(request, 'retrieve_draw.html', context)


def link_sets_draw(request):
    logger.info("Serving view for link sets draw")
    context = {}
    context['errors'] = []

    if request.method == 'POST':
        draw_form = LinkSetsForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            sets = [x.split(',') for x in [raw_draw['set_1'],raw_draw['set_2']] ]
            bom_draw = LinkSetsDraw(sets)
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
        draw_form = LinkSetsForm()

    context['draw'] = draw_form
    return render(request, 'link_sets.html', context)

def random_item_draw(request):
    logger.info("Serving view for random item draw")
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
    return render(request, 'dice_new.html', context)


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
