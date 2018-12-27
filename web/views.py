"""Definition of views for the website"""
import logging
import random
import datetime
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
import pytz
import six.moves.urllib

from django import forms
from django.template import loader
from django.http.response import JsonResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import render, resolve_url
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from pusher import Pusher

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
    shared_draws = MONGO.get_draws_with_filter({"is_shared": True})
    context = {'shared_draws': shared_draws}
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
def index(request, is_shared=None):
    """landpage"""
    context = {}
    if is_shared:
        context['is_shared'] = True
    sentence = random.choice(SENTENCES)
    context["sentence"] = {
        "image": static("img/sentences/" + str(sentence[1])),
        "alt": sentence[1],
        "text": sentence[0]
    }
    return render(request, 'index.html', context)


@time_it
def create_draw(request, draw_type, is_shared):
    """create_draw view

    Servers the page to create a draw
    """
    if draw_type == 'spinner':
        return render(request, 'draws/create_spinner.html', {})

    is_shared = is_shared or is_shared == 'True'
    LOG.debug("Serving view to create a draw: {0}".format(draw_type))
    try:
        initial = request.GET.copy()
        initial['is_shared'] = is_shared
        draw_form = draw_factory.create_form(draw_type,
                                             initial=initial)
    except draw_factory.DrawNotRegistered as e:
        return HttpResponseNotFound("Draw type not registered: " + str(e))
    return render(request, 'draws/new_draw.html',
                  {"draw": draw_form, "is_shared": is_shared,
                   "draw_type": draw_type,
                   "default_title": draw_form.DEFAULT_TITLE})


@time_it
def display_draw(request, draw_id):
    """Returns the data to display a draw
    Given a draw id, retrieves it and returns the data required to display it
    """
    bom_draw = MONGO.retrieve_draw(draw_id)
    if bom_draw.draw_type == 'spinner':
        return render(request, "draws/display_spinner.html", {"bom": bom_draw})

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    if bom_draw.check_read_access(request.user):
        generated_results = False
        for result in bom_draw.results:
            if ("publication_datetime" in result and "items" not in result
                    and now > result["publication_datetime"]):
                result["items"] = bom_draw.generate_result()
                generated_results = True
        if generated_results:
            LOG.info("Generated results for draw {} as they were scheduled"
                    .format(bom_draw))
            MONGO.save_draw(bom_draw)
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


pusher = Pusher(app_id=u'163051', key=u'61af23772ca14dff55e5', secret=settings.PUSHER_SECRET)


@csrf_exempt
def pusher_authenticate(request):
    """Authentication end point for pusher priv channels"""
    if request.POST and 'channel_name' in request.POST:
        data = request.POST
    else:
        data = six.moves.urllib.parse.parse_qs(request.body)
        data = {k: v[0] for k,v in data.items()}
    channel = data['channel_name']
    socket_id = data['socket_id']
    auth = pusher.authenticate(channel=channel, socket_id=socket_id)
    return JsonResponse(auth)


# from: http://code.runnable.com/UqMu5Wsrl3YsAAfX/using-django-s-built-in-views-for-password-reset-for-python
class MongoSetPasswordForm(SetPasswordForm):
    """Set form with our logic for mongo"""
    def save(self, commit=True):
        user = MONGO.retrieve_user(self.user.pk)
        user.set_password(self.cleaned_data['new_password1'])
        MONGO.save_user(user)
        return self.user


class MongoResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, subject_template_name, email_template_name,
             token_generator=default_token_generator,
             html_email_template_name=None, **_):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        user = MONGO.retrieve_user(email)
        c = {
            'email': user.email,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
        }
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)

        if html_email_template_name:
            html_email = loader.render_to_string(html_email_template_name, c)
        else:
            html_email = None
        send_mail(subject, email, "reset_password@echaloasuerte.com", [user.email], html_message=html_email)


def reset(request):
    """Wrap the built-in password reset view and pass it the arguments
    like the template name, email template name, subject template name
    and the url to redirect after the password reset is initiated."""
    return password_reset(request, template_name='reset.html',
        email_template_name='reset_email.html',
        html_email_template_name='reset_email.html',
        subject_template_name='reset_subject.txt',
        password_reset_form=MongoResetForm,
        post_reset_redirect=reverse('reset_success'))


def reset_confirm(request, uidb64=None, token=None):
    """Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    and template name, url to redirect after password reset is confirmed."""
    return password_reset_confirm(request, template_name='reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('login'))

# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=MongoSetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = MONGO.retrieve_user(uid)
    except (TypeError, ValueError, OverflowError, MONGO.NotFoundError):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
        }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
