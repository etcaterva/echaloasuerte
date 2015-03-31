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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.core.mail import send_mail
from contextlib import contextmanager
import logging
import time

logger = logging.getLogger("echaloasuerte")
mongodb = MongoDriver.instance()


@contextmanager
def scoped_timer(func_name):
    st = time.time()
    yield
    elapsed = time.time() - st
    logger.debug("{1} completed in {0:.2f}ms.".format(elapsed,func_name))

def minimice(data):
    """Reduces the amount of info for some types of object"""
    if isinstance(data,HttpRequest):
        return dict(user=data.user.pk, post=data.POST, get=data.GET)
    else:
        return data

def time_it(func):
    """decorator to add trace information"""
    def _(*args,**kwargs):
        min_args = [minimice(x) for x in args]
        min_kwargs = {k:minimice(x) for k,x in kwargs.items()}
        logger.debug("Calling: {0} with args: {1}, and kwargs {2}".format(func.__name__,min_args,min_kwargs))
        with scoped_timer(func.__name__):
            return func(*args,**kwargs)
    return _



def find_previous_version(curr_draw):
    """
    Search in the DB for a previous draw with the same id. If found, the old and current version are compared.
    If the draw configuration didn't change returns the old version so later the results will be added to this one
    Otherwise it will clean the draw id (so mongo will assign a new one to it later). A link to the older version of the
    draw is added.
    """
    IGNORED_FIELDS = ('creation_time', 'number_of_results',
                  'results', '_id', 'draw_type', 'prev_draw',
                  'users', 'password', 'title', 'shared_type')  # 'owner',
    if curr_draw._id == '':
        curr_draw._id = None
        logger.info("There is not a previous version of this draw in the DB")
        return curr_draw
    logger.info("ID current draw: {0}".format(curr_draw._id))
    prev_draw = mongodb.retrieve_draw(curr_draw.pk)
    for k, v in curr_draw.__dict__.items():
        if k not in IGNORED_FIELDS and (
                k not in prev_draw.__dict__.keys() or v != prev_draw.__dict__[k]):
            # Data have changed
            logger.info("Old draw with id {0} changed on key {1}. Old '{2}', new '{3}'".format(prev_draw._id, k,prev_draw.__dict__.get(k,"Empty"),v))
            curr_draw.prev_draw = prev_draw._id
            # Clean the current's draw id, so a new one will be assigned to it
            curr_draw._id = None
            return curr_draw
    # Data haven't changed so return previous draw to work on it
    logger.info("There is a previous version of this draw in the DB {0}".format(prev_draw._id, k))

    #updatable fields of prev draw
    UPDATE_FIELDS=('password', 'shared_type', 'title', 'users', 'number_of_results')
    for k in UPDATE_FIELDS:
        prev_draw.__dict__[k] = curr_draw.__dict__[k]
    return prev_draw


def user_can_read_draw(user,draw,password = None):
    '''Validates that user can read draw. Throws unauth otherwise'''
    if not draw.user_can_read(user,password):
        logger.info("User {0} not allowed to read draw {1}. Type: {2}, Password? {3}, Owner:{4}, Users: {5}"
                .format(user.pk, draw.pk, draw.shared_type, 'Y' if draw.password else 'N', draw.owner, draw.users))
        raise PermissionDenied()

def user_can_write_draw(user,draw):
    if not draw.user_can_write(user):
        logger.info("User {0} not allowed to write draw {1}. Type: {2}, Password? {3}, Owner:{4}"
                .format(user.pk, draw.pk, draw.shared_type, 'Y' if draw.password else 'N', draw.owner))
        raise PermissionDenied()

def set_owner(draw, request):
    """Best effort to set the owner given a request"""
    try:
        draw.owner = request.user.pk
    except:
        pass

@time_it
def login_user(request):
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


@time_it
def register(request):
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
@time_it
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
        bom_draw.users.append(user.pk)
    invite_user(user_list, draw_id,request.user.get_email())

    logger.info("{0} users added to draw {1}".format(len(user_list),draw_id))

    return HttpResponse()

@login_required
@time_it
def add_favorite(request):
    draw_id = request.GET.get('draw_id',None)

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = mongodb.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw) #raises 500
    user = mongodb.retrieve_user(request.user.pk)
    if draw_id in user.favourites:
        logger.info("Draw {0} is favorite for user {1}".format(draw_id, request.user.pk))
        return HttpResponse()

    user.favourites.append(draw_id)
    mongodb.save_user(user)

    logger.info("Draw {0} added as favorite for user {1}".format(draw_id, request.user.pk))
    return HttpResponse()


@login_required
@time_it
def remove_favorite(request):
    draw_id = request.GET.get('draw_id',None)

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = mongodb.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw) #raises 500
    user = mongodb.retrieve_user(request.user.pk)
    if draw_id not in user.favourites:
        logger.info("Draw {0} is not favorite for user {1}".format(draw_id, request.user.pk))
        return HttpResponse()

    user.favourites.remove(draw_id)
    mongodb.save_user(user)

    logger.info("Draw {0} removed as favorite for user {1}".format(draw_id, request.user.pk))
    return HttpResponse()


@login_required
@time_it
def change_privacy_draw(request):
    draw_id = request.GET.get('draw_id', None)
    shared_type = request.GET.get('shared_type', None)
    password = request.GET.get('password', None)

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = mongodb.retrieve_draw(draw_id)

    if shared_type == "Public" or shared_type == "Invite":
        bom_draw.shared_type = shared_type
        if password:
            bom_draw.password = password
    else:
        logger.warning("Wrong type of public draw: {0}".format(shared_type))
        return HttpResponse("KO")


@login_required
@time_it
def profile(request):
    draws = []
    try:
        draws = mongodb.get_user_draws(request.user._id)
    except Exception as e:
        logger.error("There was an issue when retrieving user draws. {0}".format(e))

    context = {'draws': draws}
    return render(request, 'profile.html', context)

@time_it
def join_draw(request):
    """view to show the list of draws a user can join"""
    public_draws = []
    user_draws = []
    try:
        public_draws = mongodb.get_draws_with_filter({
            "shared_type":"Public",
            })
    except Exception as e:
        logger.error("There was an issue when retrieving public draws. {0}".format(e))
    if request.user.is_authenticated():
        try:
            user_draws = mongodb.get_draws_with_filter({
                "$and" : [
                    { "$or" : [{"shared_type" : "Public"},  {"shared_type" : "Invite"} ] },
                    { "$or" : [{"owner" : request.user.pk}, {"user": request.user.pk}  ] }
                    ]
                })
        except Exception as e:
            logger.error("There was an issue when retrieving user draws. {0}".format(e))

    context = {'public_draws': public_draws, 'user_draws' : user_draws}
    return render(request, 'join_draw.html', context)

@time_it
def index(request, is_public=None):
    context = {}
    if is_public:
        context['is_public'] = 'publish'
        context['public_draw_step'] = 'choose'
    return render(request, 'index.html', context)

URL_TO_DRAW_MAP = {
    'coin': 'CoinDraw',
    'dice': 'DiceDraw',
    'card': 'CardDraw',
    'number': 'RandomNumberDraw',
    'item': 'RandomItemDraw',
    'link_sets': 'LinkSetsDraw',
}

DRAW_TO_URL_MAP ={ v:k for k,v in URL_TO_DRAW_MAP.items()}

@time_it
def retrieve_draw(request, draw_id):
    bom_draw = mongodb.retrieve_draw(draw_id)
    return draw(request, DRAW_TO_URL_MAP[bom_draw.draw_type], draw_id)

@time_it
def draw(request, draw_type=None,  draw_id=None, publish=None):
    # Based on "draw_type" parameter, get the name of it's model
    model_name = URL_TO_DRAW_MAP[draw_type]
    # Based on the model's name, get the name of the form
    form_name = model_name + "Form"
    # Create an empty draw object (based on the parameter "draw_type")
    bom_draw = globals()[model_name]()
    context = {'errors': [], 'can_write': True}
    if publish:
        # The variable is_public is used decide whether to render the single user draw or the public draw interface
        # It's only declared if the draw is public.
        context['is_public'] = 'publish'
        # The variable "public_draw_step" is used to decide which step has to be rendered while creating a public draw
        # It's only declared during the process of creation (does not exists when the draw is published)
        # It's set to configure since the step "choose" has already been done in the view "index"
        context['public_draw_step'] = 'configure'
        logger.info("Creating public draw. Step finished: Choose type of draw")

    if request.method == 'POST':
        # The ways to reach here is either by performing a toss or being in the process of configuring a public draw
        logger.debug("Received post data: {0}".format(request.POST))
        # Create a form (based on the parameter "draw_type") and load in it the data coming in the POST
        draw_form = globals()[form_name](request.POST)
        if draw_form.is_valid():
            # Obtain the data from the form
            raw_draw = draw_form.cleaned_data
            logger.debug("Form cleaned data: {0}".format(raw_draw))
            # Create a draw object with the data coming in the POST
            bom_draw = globals()[model_name](**raw_draw)
            # When the draw is public, the variable "is_public" will be send to the template
            if bom_draw.shared_type != "None":
                context['is_public'] = 'publish'
            # If bom_draw.id == '' the user has filled the fields manually so the draw will be consider as a new one
            # and the user who is doing the POST will own it.
            if bom_draw.pk == '':
                set_owner(bom_draw, request)

            # If the user has not writing right on the draw, a exception will rise (as he can not POST on it)
            user_can_write_draw(request.user, bom_draw)

            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                #check type of submit
                submit_type = request.POST.get("submit-type","EMPTY").lower()
                if submit_type == "toss":
                    # Tossing a normal draw
                    bom_draw.toss()
                    logger.info("Generating result for draw {0}".format(bom_draw.pk))

                elif submit_type == "go_to_spread":
                    # Configuration has been done. Next step is spread
                    # TODO return the draw's id
                    context['public_draw_step'] = 'spread'
                    logger.info("Creating public draw {0}. Step finished: Configure".format(bom_draw.pk))

                elif submit_type == "publish":
                    # The draw is configured. Make it public
                    bom_draw.results = []
                    logger.info("Created public draw {0}. Cleaned up trial results.".format(bom_draw.pk))
                    mongodb.save_draw(bom_draw)
                    # The user is redirected to the draw he has created
                    return redirect('draw', draw_type=draw_type, draw_id=bom_draw.pk)

                elif submit_type == "edit_public_draw":
                    # The user has edited a public draw.
                    # Check whether it differ from the old version
                    if draw_form.data['_id'] != bom_draw.pk:
                        bom_draw.results = []
                        logger.info("The configuration of the public draw {0} has changed. Created new one {1}.".format(draw_form.data['_id'], bom_draw.pk))
                        mongodb.save_draw(bom_draw)
                        # The user is redirected to the draw he has created
                        return redirect('draw', draw_type=draw_type, draw_id=bom_draw.pk)

                elif submit_type == "public_toss":
                    # It's a public draw and the button Toss has been clicked
                    bom_draw.toss()
                    logger.info("Generated result for public draw {0}.".format(bom_draw.pk))

                elif submit_type == "try":
                    # While configuring a public draw, "Try" button has been clicked
                    bom_draw.toss()
                    logger.info("Generating test result for draw {0}".format(bom_draw.pk))

                else:
                    logger.error("Invalid submit type: {0}. It will be considered as toss".format(submit_type))
                    bom_draw.toss()

                mongodb.save_draw(bom_draw)
                # Update the draw's id in the form
                # The configuration may be changed by the user. If so, a new draw is generated so the id needs to be updated.
                # The dictionary "data" needs to be copied since the POST variable is immutable
                draw_form.data = draw_form.data.copy()
                draw_form.data['_id'] = bom_draw.pk
                logger.debug("Generated draw: {0}".format(bom_draw))
            else:
                logger.info("Draw {0} is not feasible".format(bom_draw))
                context['errors'].append(_("The draw is not feasible"))
        else:
            logger.info("Form not valid")
            logger.debug("Errors in the form: {0}".format(draw_form.errors))
    else:
        if draw_id:
            # The user is retrieving a draw (it can be public or for a single user)
            bom_draw = mongodb.retrieve_draw(draw_id)
            user_can_read_draw(request.user, bom_draw,request.GET.get("password", default=None))
            logger.debug("Filling form with retrieved draw {0}".format(bom_draw))
            if bom_draw.draw_type == model_name:
                # If the draw is public, the variable is_public is send to the template
                if not bom_draw.shared_type is None:
                    context['is_public'] = 'publish'
                draw_form = globals()[form_name](initial=bom_draw.__dict__)
            else:
                logger.info("Draw type mismatch, type: {0}".format(bom_draw.draw_type))
                raise Http404
        else:
            #Serve to create Draw
            draw_form = globals()[form_name]()

    context['can_write'] = bom_draw.user_can_write(request.user)
    context['draw'] = draw_form
    context["bom"] = bom_draw
    template_path = 'draws/{0}.html'.format(model_name)
    return render(request, template_path, context)


@time_it
def under_construction(request):
    return render(request, 'under_construction.html', {})
