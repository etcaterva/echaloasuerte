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
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib import messages
from web.common import user_can_read_draw, user_can_write_draw, time_it
import logging

logger = logging.getLogger("echaloasuerte")
mongodb = MongoDriver.instance()


def find_previous_version(curr_draw):
    """
    Search in the DB for a previous draw with the same id. If found, the old and current version are compared.
    If the draw configuration didn't change returns the old version so later the results will be added to this one
    Otherwise it will clean the draw id (so mongo will assign a new one to it later). A link to the older version of the
    draw is added.
    """
    IGNORED_FIELDS = ('creation_time', 'last_updated_time', 'number_of_results',
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

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if 'keep-logged' in request.POST:
                    request.session.set_expiry(31556926)  # 1 year
                logger.info("expiration" + str(request.session.get_expiry_date()))
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                context = {'error': "User is not activated yet"}
        else:
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
    if request.user.is_authenticated():
        user = request.user.pk
        user_draws = mongodb.get_draws_with_filter({
            "$and" : [
                { "$or" : [{"shared_type" : "Public"},  {"shared_type" : "Invite"} ] },
                { "$or" : [{"owner" : request.user.pk}, {"user": request.user.pk}  ] }
            ]
        })
    try:
        public_draws = mongodb.get_draws_with_filter(
                {"shared_type": "Public","show_in_public_list": True},
            )
    except Exception as e:
        logger.error("There was an issue when retrieving public draws. {0}".format(e))
    user_draws_pk = [draw.pk for draw in user_draws]
    public_draws = [draw for draw in public_draws if draw.pk not in user_draws_pk]
    public_draws = public_draws + user_draws
    context = {'public_draws': public_draws}
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

#TODO:
# - Remove this first retrieve_draw that just redirect to draw
# - Wrap the creation of draws and form through a factory. No more global
# - Move is_feasible to the form validation
# - Wrap "draw" config data in group so we can check in a single instruction if
#       a draw changed
# - Change user_can_read and write to methods
# - Add ws to validate a bom without creating it

@time_it
def retrieve_draw(request, draw_id):
    bom_draw = mongodb.retrieve_draw(draw_id)
    return draw(request, DRAW_TO_URL_MAP[bom_draw.draw_type], draw_id)


@time_it
def toss_draw(request):
    """generates and saves a result
    The id of the draw to toss is present as a POST attribute
    redirects to the draw to display
    """
    bom_draw = mongodb.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)
    bom_draw.toss()
    mongodb.save_draw(bom_draw)
    return redirect('retrieve_draw', draw_id=bom_draw.pk)


@time_it
def create_draw(request, draw_type, is_public):
    """create_draw view
    @param
    Serves the page to create a draw (empty) form
        and handles the creation of a draw.
    When received a GET request returns an empty form to create a draw
        and with a POST and data attempts to create a draw. If success,
        redirects to the draw, otherwise, returns the form with the errors.
    """
    model_name = URL_TO_DRAW_MAP[draw_type]
    form_name = model_name + "Form"
    is_public = is_public == 'True'

    if request.method == 'GET':
        logger.debug("Serving view to create a draw. Form: {0}".format(form_name))
        draw_form = globals()[form_name]()
        return render(request, 'draws/new_draw.html', {"draw" : draw_form, "is_public": is_public, "draw_type": model_name, "default_title": "New Draw"})
    else:
        logger.debug("Received post data: {0}".format(request.POST))
        draw_form = globals()[form_name](request.POST)
        if not draw_form.is_valid():
            logger.info("Form not valid: {0}".format(draw_form.errors))
            messages.error(request, _('Invalid values provided'))
            return render(request, 'draws/new_draw.html', {"draw" : draw_form, "is_public": is_public, "draw_type": model_name })
        else:
            raw_draw = draw_form.cleaned_data
            logger.debug("Form cleaned data: {0}".format(raw_draw))
            # Create a draw object with the data coming in the POST
            bom_draw = globals()[model_name](**raw_draw)
            bom_draw._id = None # Ensure we have no id
            set_owner(bom_draw, request)
            if not bom_draw.is_feasible(): # This should actually go in the form validation
                logger.info("Draw {0} is not feasible".format(bom_draw))
                messages.error(request, _('The draw is not feasible'))
                return render(request, 'draws/new_draw.html', {"draw" : draw_form, "is_public": is_public, "draw_type": model_name })
            else:
                #generate a result if a private draw
                if not bom_draw.is_shared():
                    bom_draw.toss()
                mongodb.save_draw(bom_draw)
                logger.info("Generated draw: {0}".format(bom_draw))
                messages.error(request, _('Draw created successfully'))
                return redirect('retrieve_draw', draw_id=bom_draw.pk)


@time_it
def update_draw(request, draw_id):
    """Serves the update of a draw
    @draw_id: pk of the draw to update
    Given the draw details through the POST data, updates the draw.
    If success, redirects to display the view, otherwise, returns
        the form with the errors. It always create a new version
        of the draw. Use ws to update parts of the draw without
        creating a new version
    """
    prev_bom_draw = mongodb.retrieve_draw(draw_id)
    model_name = prev_bom_draw.draw_type
    form_name = model_name + "Form"
    user_can_write_draw(request.user, prev_bom_draw,request.GET.get("password"))
    template_path = 'draws/{0}.html'.format(model_name)

    if request.method == 'GET':
        logger.debug("Serving view to update a draw")
        draw_form = globals()[form_name](initial=prev_bom_draw.__dict__)
        return render(request, template_path, {"draw": draw_form})
    else:
        logger.debug("Received post data: {0}".format(request.POST))
        draw_form = globals()[form_name](request.POST)
        if not draw_form.is_valid():
            logger.info("Form not valid: {0}".format(draw_form.errors))
            messages.error(request, _('Invalid values provided'))
            return render(request, template_path, {"draw" : draw_form})
        else:
            raw_draw = draw_form.cleaned_data
            logger.debug("Form cleaned data: {0}".format(raw_draw))
            # Create a draw object with the data coming in the POST
            bom_draw = globals()[model_name](**raw_draw)
            bom_draw._id = None #Ensure we create a new draw
            bom_draw.prev_draw = prev_bom_draw.pk
            if not bom_draw.is_feasible(): # This should actually go in the form validation
                logger.info("Draw {0} is not feasible".format(bom_draw))
                messages.error(request, _('The draw is not feasible'))
                return render(request, template_path,{"draw" : draw_form })
            else:
                mongodb.save_draw(bom_draw)
                logger.info("Generated draw: {0}".format(bom_draw))
                messages.error(request, _('Draw updated successfully'))
                return redirect('retrieve_draw', draw_id=bom_draw.pk)


@time_it
def display_draw(request, draw_id):
    """Returns the data to display a draw
    Given a draw id, retrieves it and returns the data required to display it
    """
    bom_draw = mongodb.retrieve_draw(draw_id)
    model_name = bom_draw.draw_type
    form_name = model_name + "Form"
    user_can_read_draw(request.user, bom_draw,request.GET.get("password"))
    draw_form = globals()[form_name](initial=bom_draw.__dict__)
    return render(request, "draws/display_draw.html", {"draw": draw_form, "bom": bom_draw})


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

        # When a public draw is going to be created, the shared type will be "Public" by default (instead of "None")
        bom_draw.shared_type = "Public"
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
            user_can_write_draw(request.user, bom_draw)
            set_owner(bom_draw, request)
            bom_draw = find_previous_version(bom_draw)
            if bom_draw.is_feasible():
                #check type of submit
                submit_type = request.POST.get("submit-type","EMPTY").lower()
                if submit_type == "toss":
                    # Tossing a normal draw
                    bom_draw.toss()
                    logger.info("Generating result for draw {0}".format(bom_draw.pk))
                    mongodb.save_draw(bom_draw)
                    # The user is redirected to the draw he has created
                    return redirect('draw', draw_type=draw_type, draw_id=bom_draw.pk)

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
            return redirect('retrieve_draw', draw_id=draw_id)
        else:
            # Even though it's a new form, some fields may have been preset before (i.e shared_type field)
            draw_form = globals()[form_name](initial=bom_draw.__dict__)

    context['can_write'] = bom_draw.user_can_write(request.user)
    context['draw'] = draw_form
    context["bom"] = bom_draw
    template_path = 'draws/{0}.html'.format(model_name)
    return render(request, template_path, context)


@time_it
def under_construction(request):
    return render(request, 'under_construction.html', {})
