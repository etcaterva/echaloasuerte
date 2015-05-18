"""definition of basic web services"""

import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse, \
                        HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from server.mongodb.driver import MongoDriver
from web.common import user_can_read_draw, user_can_write_draw, time_it


LOG = logging.getLogger("echaloasuerte")
MONGO = MongoDriver.instance()


def ws_try_draw(request, draw_id):
    """generates a result and returns it"""
    bom_draw = MONGO.retrieve_draw(draw_id)
    return bom_draw.toss()


@login_required
def add_user_to_draw(request):
    """Add an user to a draw and sends a mail to inform him"""
    draw_id = request.GET.get('draw_id')
    users_to_add = request.GET.get('emails', [])

    if draw_id is None:
        return HttpResponseBadRequest()

    LOG.info("Adding {0} to draw {1}".format(users_to_add, draw_id))
    bom_draw = MONGO.retrieve_draw(draw_id)

    user_can_write_draw(request.user, bom_draw) # Raises 500

    new_users = users_to_add.replace(',', ' ').split()

    try:
        for email in new_users:
            validate_email(email)  # Raises a ValidationError
    except ValidationError:
        LOG.info("One or more emails are not correct")
        return HttpResponseBadRequest()

    bom_draw.users += new_users
    MONGO.save_draw(bom_draw)

    # TODO send emails to the users in the list "new_users"
    # invite_user(new_users, draw_id, request.user.get_email())

    LOG.info("{0} users added to draw {1}".format(len(new_users), draw_id))

    return HttpResponse()


@login_required
def add_favorite(request):
    """Add a draw to the list of favourites of an user"""
    draw_id = request.GET.get('draw_id')

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw) #raises 500
    user = MONGO.retrieve_user(request.user.pk)
    if draw_id in user.favourites:
        LOG.info("Draw {0} is favorite for user {1}".format(
            draw_id, request.user.pk))
        return HttpResponse()

    user.favourites.append(draw_id)
    MONGO.save_user(user)

    LOG.info("Draw {0} added as favorite for user {1}".format(
        draw_id, request.user.pk))
    return HttpResponse()


@login_required
def remove_favorite(request):
    """removes a draw from the list of favourites"""
    draw_id = request.GET.get('draw_id')

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw) #raises 500
    user = MONGO.retrieve_user(request.user.pk)
    if draw_id not in user.favourites:
        LOG.info("Draw {0} is not favorite for user {1}".format(
            draw_id, request.user.pk))
        return HttpResponse()

    user.favourites.remove(draw_id)
    MONGO.save_user(user)

    LOG.info("Draw {0} removed as favorite for user {1}".format(
        draw_id, request.user.pk))
    return HttpResponse()

def check_access_to_draw(request):
    """Checks whether an user can access to a draw"""
    draw_id = request.GET.get('draw_id')
    password = request.GET.get('draw_pass')
    draw = MONGO.retrieve_draw(draw_id)

    user_can_read_draw(request.user, draw, password)
    return HttpResponse()

def add_message_to_chat(request):
    """Adds a message to a chat"""
    draw_id = request.GET.get('draw_id')
    message = request.GET.get('message')
    user = request.user.pk
    MONGO.add_chat_message(draw_id, message, user)
    return HttpResponse()

def get_chat_messages(request):
    draw_id = request.GET.get('draw_id')
    try:
        messages = MONGO.retrieve_chat_messages(draw_id)
    except MongoDriver.NotFoundError:
        messages = []

    return JsonResponse({
        "messages" : messages
        })

@login_required
def change_privacy_public_draw(request):
    draw_id = request.GET.get('draw_id')
    shared_type = request.GET.get('shared_type')
    password = request.GET.get('password')

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = MONGO.retrieve_draw(draw_id)

    if shared_type == "Public" or shared_type == "Invite":
        bom_draw.shared_type = shared_type
        bom_draw.password = password
        MONGO.save_draw(bom_draw)
        LOG.info("The type of the public draw {0} has changed to {1}".format(
            draw_id, shared_type))
        return HttpResponse()
    else:
        LOG.warning("Wrong type of public draw: {0}".format(shared_type))
        return HttpResponseBadRequest()


