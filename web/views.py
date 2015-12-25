"""Definition of views for the website"""
import logging
import random

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

from server import draw_factory
from server.mongodb.driver import MongoDriver
from web.common import time_it

LOG = logging.getLogger("echaloasuerte")
MONGO = MongoDriver.instance()


@login_required
@time_it
def profile(request):
    """Web with the details of an user"""
    draws = []
    try:
        draws = MONGO.get_user_draws(request.user.pk)
    except Exception as e:
        LOG.error(
            "There was an issue when retrieving user draws. {0}".format(e))

    context = {'draws': draws}
    return render(request, 'profile.html', context)


@time_it
def join_draw(request):
    """view to show the list of draws a user can join"""
    public_draws = MONGO.get_draws_with_filter({"is_shared": True})
    context = {'public_draws': public_draws}
    return render(request, 'join_draw.html', context)


# stores pairs of sentences and image url under static/img/sentences/
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


@time_it
def create_draw(request, draw_type, is_public):
    """create_draw view

    Servers the page to create a draw
    """

    is_public = is_public or is_public == 'True'

    if request.method == 'GET':
        LOG.debug("Serving view to create a draw: {0}".format(draw_type))
        draw_form = draw_factory.create_form(draw_type,
                                             initial={'is_shared': is_public})
        return render(request, 'draws/new_draw.html',
                      {"draw": draw_form, "is_public": is_public,
                       "draw_type": draw_type,
                       "default_title": draw_form.DEFAULT_TITLE})
    else:
        LOG.error(
            "Deprecated draw creation, the api should have been used instead")


@time_it
def display_draw(request, draw_id):
    """Returns the data to display a draw
    Given a draw id, retrieves it and returns the data required to display it
    """
    bom_draw = MONGO.retrieve_draw(draw_id)
    if bom_draw.check_read_access(request.user):
        draw_data = bom_draw.__dict__.copy()
        draw_form = draw_factory.create_form(bom_draw.draw_type, initial=draw_data)
        return render(request, "draws/display_draw.html",
                      {"draw": draw_form, "bom": bom_draw})
    else:
        return render(request, "draws/secure_draw.html", {"bom": bom_draw})


@time_it
def under_construction(request):
    """under construction page. This should be temporary"""
    return render(request, 'under_construction.html', {})
