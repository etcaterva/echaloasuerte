"""Definition of views for the website"""
from django.http import *
from server.bom import *
from server.forms import *
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from server.bom.user import User
from server.mongodb.driver import MongoDriver
from server.forms.form_base import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.templatetags.static import static
from web.common import user_can_read_draw, user_can_write_draw, time_it, invite_user
import logging
from web.google_analytics import ga_track_event

LOG = logging.getLogger("echaloasuerte")
MONGO = MongoDriver.instance()


def set_owner(draw, request):
    """Best effort to set the owner given a request"""
    try:
        draw.owner = request.user.pk
    except:
        pass


@time_it
def login_user(request):
    """Serves logging web site
    Serves a page with data to log in
    If post data is provided, logs the user in
    """
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
                LOG.info("expiration" + str(request.session.get_expiry_date()))
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                context = {'error': "User is not activated yet"}
        else:
            context = {'error': "Email or password not valid."}
    return render(request, 'login.html', context)


@time_it
def register(request):
    """Registers a user
    Serves a web to register the user
    Register and logs the user in if POST data is provided
    """
    logout(request)
    context = {}
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        u = User(email)
        u.set_password(password)
        try:
            MONGO.create_user(u)
            ga_track_event(category="user", action="registration")
            return login_user(request)
        except Exception:
            context = {'error': _("The email is already registered.")}
    return render(request, 'register.html', context)


@login_required
@time_it
def profile(request):
    """Web with the details of an user"""
    draws = []
    try:
        draws = MONGO.get_user_draws(request.user.pk)
    except Exception as e:
        LOG.error("There was an issue when retrieving user draws. {0}".format(e))

    context = {'draws': draws}
    return render(request, 'profile.html', context)


@time_it
def join_draw(request):
    """view to show the list of draws a user can join"""
    public_draws = MONGO.get_draws_with_filter({"is_shared": True})
    context = {'public_draws': public_draws}
    return render(request, 'join_draw.html', context)


# stores pairs of sentences and image url undder static/img/sentences/
SENTENCES = (
    (_("10 seconds, which wire should you cut?"), "dinamite.png"),
    (_("Who takes care of the trash?"), "basura.png"),
    (_("Not sure what to answer in the IQ test?"), "personalidad.png"),
    (_("Dont reach an agrement with the name of the dog?"), "perro.png"),
    (_("Not sure about inviting her/him to the weeding?"), "boda.png"),
    (_("What should you cook today?"), "cocinero.png"),
    (_("Who is paying this round?"), "cerveza.png"),
    (_("Who will take the best bed?"), "cama.png"),
    (_("Not enough cake for everybody?"), "tarta.png"),
    (_("Who are you meeting tonight?"), "beso.png"),
    (_("What game are you playing today?"), "juego.png"),
    (_("Whose fault is it?"), "enfado.png"),
    (_("What subject are you failing this year?"), "asignatura.png"),
    (_("Should you quite smoking?"), "cigarrillo.png"),
    (_("Who drinks next?"), "tequila.png"),
    (_("Charmander, bulbasaur or Squirtle??"), "pokemon.png"),
    (_("What cell to start?"), "buscaminas.png"),
)


@time_it
def index(request, is_public=None):
    """landpage"""
    context = {}
    if is_public:
        context['is_public'] = True
    sentence = random.choice(SENTENCES)
    context["sentence"] = {
        "image": static("img/sentences/" + str(sentence[1])),
        "alt": sentence[1],
        "text": sentence[0]
    }
    return render(request, 'index.html', context)


# TODO:
# - Wrap the creation of draws and form through a factory. No more global
# - Move is_feasible to the form validation
#       a draw changed
# - Change user_can_read and write to methods


@time_it
def try_draw(request, draw_type):
    """validate the draw
    if request.POST contains "try_draw", generates a result
    """
    model_name = URL_TO_DRAW_MAP[draw_type]
    form_name = model_name + "Form"

    LOG.debug("Received post data: {0}".format(request.POST))
    draw_form = globals()[form_name](request.POST)
    if not draw_form.is_valid():
        LOG.info("Form not valid: {0}".format(draw_form.errors))
        messages.error(request, _('Invalid values provided'))
        return render(request, 'draws/new_draw.html', {"draw": draw_form, "is_public": True, "draw_type": model_name})
    else:
        raw_draw = draw_form.cleaned_data
        LOG.debug("Form cleaned data: {0}".format(raw_draw))
        bom_draw = globals()[model_name](**raw_draw)
        if not bom_draw.is_feasible():  # This should actually go in the form validation
            LOG.info("Draw {0} is not feasible".format(bom_draw))
            messages.error(request, _('The draw is not feasible'))
            return render(request, 'draws/new_draw.html',
                          {"draw": draw_form, "is_public": True, "draw_type": model_name})
        else:
            bom_draw.toss()
            return render(request, 'draws/new_draw.html',
                          {"draw": draw_form, "is_public": True, "draw_type": model_name, "bom": bom_draw})


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
    is_public = is_public or is_public == 'True'

    if request.method == 'GET':
        LOG.debug("Serving view to create a draw. Form: {0}".format(form_name))
        draw_form = globals()[form_name]()
        return render(request, 'draws/new_draw.html',
                      {"draw": draw_form, "is_public": is_public, "draw_type": model_name, "default_title": draw_form.DEFAULT_TITLE})
    else:
        LOG.debug("Received post data: {0}".format(request.POST))
        draw_form = globals()[form_name](request.POST)
        if not draw_form.is_valid():
            LOG.info("Form not valid: {0}".format(draw_form.errors))
            messages.error(request, _('Invalid values provided'))
            return render(request, 'draws/new_draw.html',
                          {"draw": draw_form, "is_public": is_public, "draw_type": model_name})
        else:
            raw_draw = draw_form.cleaned_data
            LOG.debug("Form cleaned data: {0}".format(raw_draw))
            # Create a draw object with the data coming in the POST
            bom_draw = globals()[model_name](**raw_draw)
            bom_draw._id = None  # Ensure we have no id
            set_owner(bom_draw, request)
            if not bom_draw.is_feasible():  # This should actually go in the form validation
                LOG.info("Draw {0} is not feasible".format(bom_draw))
                messages.error(request, _('The draw is not feasible'))
                return render(request, 'draws/new_draw.html',
                              {"draw": draw_form, "is_public": is_public, "draw_type": model_name})
            else:
                # generate a result if a private draw
                if not bom_draw.is_shared:
                    bom_draw.toss()

                MONGO.save_draw(bom_draw)
                LOG.info("Generated draw: {0}".format(bom_draw))
                messages.info(request, _('Draw created successfully'))
                shared_type = 'public' if bom_draw.is_shared else 'private'
                ga_track_event(category="create_draw", action=bom_draw.draw_type, label=shared_type)
                # notify users if any
                if bom_draw.users:
                    owner = bom_draw.owner if bom_draw.owner else _("An anonymous user")
                    invite_user(bom_draw.users, bom_draw.pk, owner)

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
    prev_bom_draw = MONGO.retrieve_draw(draw_id)
    model_name = prev_bom_draw.draw_type
    form_name = model_name + "Form"
    user_can_write_draw(request.user, prev_bom_draw)

    LOG.debug("Received post data: {0}".format(request.POST))
    draw_form = globals()[form_name](request.POST)
    if not draw_form.is_valid():
        LOG.info("Form not valid: {0}".format(draw_form.errors))
        messages.error(request, _('Invalid values provided'))
        return render(request, "draws/display_draw.html", {"draw": draw_form, "bom": prev_bom_draw})
    else:
        bom_draw = prev_bom_draw
        raw_draw = draw_form.cleaned_data
        LOG.debug("Form cleaned data: {0}".format(raw_draw))
        # update the draw with the data coming from the POST
        for key, value in raw_draw.items():
            if key not in ("_id", "pk") and value != "":
                setattr(bom_draw, key, value)
        if not bom_draw.is_feasible():  # This should actually go in the form validation
            LOG.info("Draw {0} is not feasible".format(bom_draw))
            messages.error(request, _('The draw is not feasible'))
            draw_form = globals()[form_name](initial=bom_draw.__dict__.copy())
            return render(request, "draws/display_draw.html", {"draw": draw_form, "bom": bom_draw})
        else:
            bom_draw.add_audit("DRAW_PARAMETERS")
            # generate a result if a private draw
            if not bom_draw.is_shared:
                bom_draw.toss()

            MONGO.save_draw(bom_draw)
            LOG.info("Updated draw: {0}".format(bom_draw))
            messages.error(request, _('Draw updated successfully'))
            return redirect('retrieve_draw', draw_id=bom_draw.pk)


@time_it
def display_draw(request, draw_id):
    """Returns the data to display a draw
    Given a draw id, retrieves it and returns the data required to display it
    """
    bom_draw = MONGO.retrieve_draw(draw_id)
    model_name = bom_draw.draw_type
    form_name = model_name + "Form"
    if bom_draw.user_can_read(request.user):
        draw_form = globals()[form_name](initial=bom_draw.__dict__.copy())
        return render(request, "draws/display_draw.html", {"draw": draw_form, "bom": bom_draw})
    else:
        return render(request, "draws/secure_draw.html", {"bom": bom_draw})


@time_it
def under_construction(request):
    """under construction page. This should be temporary"""
    return render(request, 'under_construction.html', {})
