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

logger = logging.getLogger("echaloasuerte")
mongodb = MongoDriver.instance()

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


# stores pairs of sentences and image url undder static/img/sentences/
SENTENCES = (
    (_("10 seconds, which wire should you cut?"), "dinamite.png"),
    (_("Who takes care of the trash?"), "basura.gif"),
    (_("Not sure what to answer in the IQ test?"), "personalidad.gif"),
    (_("Dont reach an agrement with the name of the dog?"), "perro.gif"),
    (_("Not sure about inviting her/him to the weeding?"), "boda.gif"),
    (_("What should you cook today?"), "cocinero.gif"),
    (_("Who is paing this round?"), "cerveza.gif"),
    (_("Who will take the best bed?"), "cama.gif"),
    (_("Not enaugh cake for everybody?"), "tarta.gif"),
    (_("Who are you meeting tonight?"), "beso.gif"),
    (_("What game are you playing today?"), "juego.gif"),
    (_("Whose fault is it?"), "enfado.gif"),
    (_("What subject are you failing this year?"), "asignatura.gif"),
    (_("Should you quite smoking?"), "cigarrillo.gif"),
    (_("Who drinks next?"), "tequila.gif"),
    (_("Charmander, bulbasaur or Squirtle??"), "pokemon.gif"),
    (_("What cell to start?"), "buscaminas.gif"),
)

@time_it
def index(request, is_public=None):
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

#TODO:
# - Wrap the creation of draws and form through a factory. No more global
# - Move is_feasible to the form validation
# - Wrap "draw" config data in group so we can check in a single instruction if
#       a draw changed
# - Change user_can_read and write to methods

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
def try_draw(request, draw_type):
    """validate the draw
    if request.POST contains "try_draw", generates a result
    """
    model_name = URL_TO_DRAW_MAP[draw_type]
    form_name = model_name + "Form"

    logger.debug("Received post data: {0}".format(request.POST))
    draw_form = globals()[form_name](request.POST)
    if not draw_form.is_valid():
        logger.info("Form not valid: {0}".format(draw_form.errors))
        messages.error(request, _('Invalid values provided'))
        return render(request, 'draws/new_draw.html', {"draw" : draw_form, "is_public": True, "draw_type": model_name })
    else:
        raw_draw = draw_form.cleaned_data
        logger.debug("Form cleaned data: {0}".format(raw_draw))
        bom_draw = globals()[model_name](**raw_draw)
        if not bom_draw.is_feasible(): # This should actually go in the form validation
            logger.info("Draw {0} is not feasible".format(bom_draw))
            messages.error(request, _('The draw is not feasible'))
            return render(request, 'draws/new_draw.html', {"draw" : draw_form, "is_public": True, "draw_type": model_name })
        else:
            bom_draw.toss()
            return render(request, 'draws/new_draw.html', {"draw" : draw_form, "is_public": True, "draw_type": model_name, "bom": bom_draw})

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
                messages.info(request, _('Draw created successfully'))

                #notify users if any
                if bom_draw.users:
                    owner = bom_draw.owner if bom_draw.owner else "Annon"
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
    prev_bom_draw = mongodb.retrieve_draw(draw_id)
    model_name = prev_bom_draw.draw_type
    form_name = model_name + "Form"
    user_can_write_draw(request.user, prev_bom_draw)

    logger.debug("Received post data: {0}".format(request.POST))
    draw_form = globals()[form_name](request.POST)
    if not draw_form.is_valid():
        logger.info("Form not valid: {0}".format(draw_form.errors))
        messages.error(request, _('Invalid values provided'))
        return render(request, "draws/display_draw.html", {"draw": draw_form, "bom": prev_bom_draw})
    else:
        bom_draw = prev_bom_draw
        raw_draw = draw_form.cleaned_data
        logger.debug("Form cleaned data: {0}".format(raw_draw))
        # update the draw with the data comming from the POST
        for key, value in raw_draw.items():
            if key not in ("_id", "pk") and value != "":
                setattr(bom_draw, key, value)
        if not bom_draw.is_feasible(): # This should actually go in the form validation
            logger.info("Draw {0} is not feasible".format(bom_draw))
            messages.error(request, _('The draw is not feasible'))
            draw_form = globals()[form_name](initial=bom_draw.__dict__.copy())
            return render(request, "draws/display_draw.html", {"draw": draw_form, "bom": bom_draw})
        else:
            bom_draw.add_audit("DRAW_PARAMETERS")
            #generate a result if a private draw
            if not bom_draw.is_shared():
                bom_draw.toss()

            mongodb.save_draw(bom_draw)
            logger.info("Updated draw: {0}".format(bom_draw))
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
    if bom_draw.user_can_read(request.user, request.GET.get("password")):
        draw_form = globals()[form_name](initial=bom_draw.__dict__.copy())
        return render(request, "draws/display_draw.html", {"draw": draw_form, "bom": bom_draw})
    else:
        return render(request, "draws/secure_draw.html", {"bom": bom_draw})

@time_it
def under_construction(request):
    return render(request, 'under_construction.html', {})
