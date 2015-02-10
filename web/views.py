from django.http import *
from server.forms import *
from django.shortcuts import render
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
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.core.mail import send_mail

logger = logging.getLogger("echaloasuerte")
mongodb = MongoDriver.instance()


def find_previous_version(curr_draw):
    """
    Search in the DB for a previous draw with the same id. If found, the old and current version are compared.
    If the draw configuration didn't change returns the old version so later the results will be added to this one
    Otherwise it will clean the draw id (so mongo will assign a new one to it later). A link to the older version of the
    draw is added.
    """
    if curr_draw._id == '':
        curr_draw._id = None
        logger.info("There is not a previous version of this draw in the DB")
        return curr_draw
    logger.info("ID nothin: {0}".format(curr_draw._id))
    prev_draw = mongodb.retrieve_draw(curr_draw.pk)
    if prev_draw.owner != curr_draw.owner: #security check
        raise PermissionDenied()
    for k, v in curr_draw.__dict__.items():
        if k not in ["creation_time", "results", "_id", "prev_draw" ] and (
                k not in prev_draw.__dict__.keys() or v != prev_draw.__dict__[k]):
            # Data have changed
            logger.info("Old draw with id {0} changed on key {1}".format(prev_draw._id, k))
            curr_draw.prev_draw = prev_draw._id
            # Clean the current's draw id, so a new one will be assigned to it
            curr_draw._id = None
            return curr_draw
    # Data haven't changed so return previous draw to work on it
    logger.info("There is a previous version of this draw in the DB {0}".format(prev_draw._id, k))
    return prev_draw


def user_can_read_draw(user,draw):
    if user.is_anonymous():
        raise PermissionDenied()
    if user._id != draw.owner:
        if user not in draw.users:
            raise PermissionDenied()

def user_can_write_draw(user,draw):
    if user._id != draw.owner:
        raise PermissionDenied()

def set_owner(draw, request):
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

        try:
            user = authenticate(username=username, password=password)
            if user.is_active:
                if 'keep-logged' in request.POST:
                    request.session.set_expiry(31556926)  # 1 year
                logger.info("expiration" + str(request.session.get_expiry_date()))
                login(request, user)
                return HttpResponseRedirect('/')
        except MongoDriver.NotFoundError:
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


INVITE_EMAIL_TEMPLATE = _("""
Hi!

You have been invited to a draw in echaloasuerte by {0}
Your link is <a href="http://www.echaloasuerte.com/draw/{1}/">http://www.echaloasuerte.com/draw/{1}/</a> .

Good Luck,
Echaloasuerte.com Team
""")

def invite_user(user_emails,draw_id,owner_user):
    logger.info("Inviting user {0} to draw {1}".format(user_email,draw_id))
    send_mail('Echaloasuerte', INVITE_EMAIL_TEMPLATE.format(owner_user,draw_id),
             'draws@echaloasuerte.com', user_email, fail_silently=True)


@login_required
def add_user_to_draw(request,draw_id,new_users):
    draw_id = request.POST.get('draw_id',None)
    new_users = request.POST.get('new_users',[])

    if draw_id is None:
        return HttpResponseBadRequest()

    logger.info("Adding {0} to draw {1}".format(new_users,draw_id))
    bom_draw = mongodb.retrieve_draw(draw_id)

    user_can_write_draw(request.user, bom_draw) #raises 500

    user_list = new_users.replace(',',' ').split()
    for user in user_list:
        bom_draw.users += user
        bom_user = mongodb.retrieve_user(user)
    invite_user(user_list, draw_id,request.user.get_email())

    logger.info("{0} users added to draw {1}".format(len(user_list),draw_id))

@login_required
def profile(request):
    logger.info("Serving profile page for user {0}".format(request.user))
    try:
        draws = mongodb.get_user_draws(request.user._id)
    except Exception as e:
        logger.error("There was an issue when retrieving user draws. {0}".format(draws))

    context = {'draws': draws}
    return render(request, 'profile.html', context)


def index(request, is_public=None):
    logger.info("Serving index page.")
    context = {}
    if is_public:
        context['is_public'] = 'publish'
    return render(request, 'index.html', context)


DRAW_TO_URL_MAP = {
    'RandomNumberDraw': 'random_number',
    'DiceDraw': 'dice',
    'CardDraw': 'card',
}


def retrieve_draw(request, draw_id):
    logger.info("Serving view for retrieve draw with id {0}".format(draw_id))
    bom_draw = mongodb.retrieve_draw(draw_id)
    target_view = DRAW_TO_URL_MAP[bom_draw.draw_type]
    return redirect(target_view, draw_id)


def coin_draw(request):
    logger.info("Serving view for coin draw")
    context = {'errors': []}
    if request.method == 'POST':
        logger.debug("Information posted. {0}".format(request.POST))
        bom_draw = CoinDraw()
        set_owner(bom_draw, request)
        result = bom_draw.toss()
        mongodb.save_draw(bom_draw)
        res = result["items"][0]
        context['result'] = res
        logger.info("New result generated for draw {0}".format(bom_draw._id))
        logger.debug("Generated draw: {0}".format(bom_draw))
    context["bom"] = bom_draw
    return render(request, 'draws/coin.html', context)


def dice_draw(request, draw_id=None, publish=None):
    logger.info("Serving view for dice draw")
    bom_draw = DiceDraw()
    context = {'errors': []}
    if publish:
        context['is_public'] = 'publish'
    if request.method == 'POST':
        draw_form = DiceDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            bom_draw = DiceDraw(**raw_draw)
            set_owner(bom_draw, request)
            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                bom_draw.toss()
                mongodb.save_draw(bom_draw)
                draw_form.data = draw_form.data.copy()
                draw_form.data['_id'] = bom_draw.pk
                if 'next' in request.POST:
                    logger.info("The draw is being published")
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
            bom_draw = mongodb.retrieve_draw(draw_id)
            user_can_read_draw(request.user, bom_draw)
            logger.debug("Filling form with retrieved draw {0}".format(bom_draw))
            if bom_draw.draw_type == "DiceDraw":
                draw_form = DiceDrawForm(initial=bom_draw.__dict__)
            else:
                logger.info("Draw type mismatch, type: {0}".format(bom_draw.draw_type))
                raise Http404
        else:
            draw_form = DiceDrawForm()

    context['draw'] = draw_form
    context["bom"] = bom_draw
    return render(request, 'draws/dice.html', context)


def card_draw(request, draw_id=None):
    logger.info("Serving view for card draw")
    bom_draw = CardDraw()
    context = {'errors': []}
    if request.method == 'POST':
        draw_form = CardDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            bom_draw = CardDraw(**raw_draw)
            set_owner(bom_draw, request)
            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                bom_draw.toss()
                mongodb.save_draw(bom_draw)
                draw_form.data = draw_form.data.copy()
                draw_form.data['_id'] = bom_draw.pk
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
            bom_draw = mongodb.retrieve_draw(draw_id)
            logger.debug("Filling form with retrieved draw {0}".format(bom_draw))
            if bom_draw.draw_type == "CardDraw":
                draw_form = CardDrawForm(initial=bom_draw.__dict__)
            else:
                logger.info("Draw type mismatch, type: {0}".format(bom_draw.draw_type))
                raise Http404
        else:
            draw_form = CardDrawForm()

    context['draw'] = draw_form
    context["bom"] = bom_draw
    return render(request, 'draws/card.html', context)


def random_number_draw(request, draw_id=None):
    logger.info("Serving view for random number draw")
    bom_draw = RandomNumberDraw()
    context = {'errors': []}

    if request.method == 'POST':
        logger.debug("Information posted. {0}".format(request.POST))
        draw_form = RandomNumberDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            bom_draw = RandomNumberDraw(**raw_draw)  #This works because form and python object have the same member names
            set_owner(bom_draw, request)
            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                bom_draw.toss()
                mongodb.save_draw(bom_draw)
                draw_form.data = draw_form.data.copy()
                draw_form.data['_id'] = bom_draw.pk
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
            bom_draw = mongodb.retrieve_draw(draw_id)
            logger.debug("Filling form with retrieved draw {0}".format(bom_draw))
            if bom_draw.draw_type == "RandomNumberDraw":
                draw_form = RandomNumberDrawForm(initial=bom_draw.__dict__)
            else:
                logger.info("Draw type mismatch, type: {0}".format(bom_draw.draw_type))
                raise Http404
        else:
            draw_form = RandomNumberDrawForm()

    context['draw'] = draw_form
    context["bom"] = bom_draw
    return render(request, 'draws/random_number.html', context)


def random_item_draw(request, draw_id=None):
    logger.info("Serving view for random item draw")
    bom_draw = RandomItemDraw()
    context = {'errors': []}

    if request.method == 'POST':
        draw_form = RandomItemDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            raw_draw["items"] = raw_draw["items"].split(',')
            bom_draw = RandomItemDraw(**raw_draw)
            set_owner(bom_draw, request)
            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                bom_draw.toss()
                mongodb.save_draw(bom_draw)
                draw_form.data = draw_form.data.copy()
                draw_form.data['_id'] = bom_draw.pk
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
            bom_draw = mongodb.retrieve_draw(draw_id)
            logger.debug("Filling form with retrieved draw {0}".format(bom_draw))
            if bom_draw.draw_type == "RandomItemDraw":
                draw_form = RandomItemDrawForm(initial=bom_draw.__dict__)
            else:
                logger.info("Draw type mismatch, type: {0}".format(bom_draw.draw_type))
                raise Http404
        else:
            draw_form = RandomItemDrawForm()

    context['draw'] = draw_form
    context["bom"] = bom_draw
    return render(request, 'draws/random_item.html', context)


def link_sets_draw(request, draw_id=None):
    logger.info("Serving view for link sets draw")
    bom_draw = LinkSetsDraw()
    context = {'errors': []}

    if request.method == 'POST':
        draw_form = LinkSetsForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            sets = [x.split(',') for x in [raw_draw['set_1'], raw_draw['set_2']]]
            bom_draw = LinkSetsDraw(sets)
            set_owner(bom_draw, request)
            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                bom_draw.toss()
                mongodb.save_draw(bom_draw)
                draw_form.data = draw_form.data.copy()
                draw_form.data['_id'] = bom_draw.pk
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
            bom_draw = mongodb.retrieve_draw(draw_id)
            logger.debug("Filling form with retrieved draw {0}".format(bom_draw))
            if bom_draw.draw_type == "LinkSets":
                draw_form = LinkSetsForm(initial=bom_draw.__dict__)
            else:
                logger.info("Draw type mismatch, type: {0}".format(bom_draw.draw_type))
                raise Http404
        else:
            draw_form = LinkSetsForm()

    context['draw'] = draw_form
    context["bom"] = bom_draw
    return render(request, 'draws/link_sets.html', context)


def under_construction(request):
    return render(request, 'under_construction.html', {})
