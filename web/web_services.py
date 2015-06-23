"""definition of basic web services"""
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.core.validators import validate_email
from server.mongodb.driver import MongoDriver
from web.common import user_can_read_draw, user_can_write_draw, time_it
from server.forms import *
from server.bom import *

LOG = logging.getLogger("echaloasuerte")
MONGO = MongoDriver.instance()

@login_required
@time_it
def update_user(request):
    """updates the details of a user"""
    user = MONGO.retrieve_user(request.user.pk)

    if "email" in request.POST:
        pass # user._id = request.POST["email"]
    if "password" in request.POST:
        user.set_password(request.POST["password"])
    if "alias" in request.POST:
        user.alias = request.POST["alias"]
    if "avatar" in request.POST:
        user.avatar = request.POST["avatar"]
    MONGO.save_user(user)

@time_it
def feedback(request):
    """sends the feedback data to the users"""
    subject = """[Echaloasuerte] Feedback ({0})""".format(request.POST["type"])
    message = """{0}\n By {1} on {2}""".format(request.POST["comment"],
                                               request.POST.get("email", "anonymous"),
                                               request.POST.get("browser"))
    mail_admins(subject, message, True)

@time_it
def toss_draw(request):
    """generates a result and returns it"""
    draw_id = request.GET.get("draw_id")
    if draw_id is None:
        return HttpResponseBadRequest()
    password = request.GET.get("password") #TODO use on user can write
    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw) #raises 500
    result = bom_draw.toss()
    MONGO.save_draw(bom_draw)
    return JsonResponse({
        "result" : result
        })

@time_it
def try_draw(request, draw_id):
    """generates a result and returns it"""
    bom_draw = MONGO.retrieve_draw(draw_id)
    return JsonResponse({
        "result" : bom_draw.toss()
        })


@login_required
@time_it
def add_user_to_draw(request):
    """Add an user to a draw and sends a mail to inform him"""
    draw_id = request.GET.get('draw_id')
    users_to_add = request.GET.get('emails', "")

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
@time_it
def remove_user_from_draw(request):
    """Remove an user from a draw"""
    draw_id = request.GET.get('draw_id')
    users = request.GET.get('emails', "")

    if draw_id is None:
        return HttpResponseBadRequest()

    LOG.info("Removing {0} from draw {1}".format(users, draw_id))
    bom_draw = MONGO.retrieve_draw(draw_id)

    user_can_write_draw(request.user, bom_draw) # Raises 500

    remove_users = users.replace(',', ' ').split()
    bom_draw.users = [email for email in bom_draw.users
                      if email not in remove_users]
    MONGO.save_draw(bom_draw)

    return HttpResponse()


@login_required
@time_it
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
@time_it
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


#@time_it
def get_draw_details(request):
    draw_id = request.GET.get('draw_id')
    draw = MONGO.retrieve_draw(draw_id)
    try:
        messages = MONGO.retrieve_chat_messages(draw_id)
    except MongoDriver.NotFoundError:
        messages = []

    return JsonResponse({
        "messages" : messages,
        "settings" : draw.share_settings,
        "last_updated_time" : draw.last_updated_time
        })

@time_it
def validate_draw(request):
    """WS to validate a draw"""
    draw_type = request.POST.get("draw_type")
    model_name = draw_type
    form_name = draw_type + "Form"

    logger.debug("Received post data: {0}".format(request.POST))
    draw_form = globals()[form_name](request.POST)
    if not draw_form.is_valid():
        logger.info("Form not valid: {0}".format(draw_form.errors))
        return JsonResponse({
            "is_valid" : False,
            "errors": draw_form.errors
            })
    else:
        raw_draw = draw_form.cleaned_data
        logger.debug("Form cleaned data: {0}".format(raw_draw))
        bom_draw = globals()[model_name](**raw_draw)
        if not bom_draw.is_feasible():
            logger.info("Draw {0} is not feasible".format(bom_draw))
            return JsonResponse({
                "is_valid" : False,
                "errors": "Not feasiible"
                })
        else:
            return JsonResponse({
                "is_valid" : True,
                })


@time_it
def update_share_settings(request):
    """Updates the shared settings.

    input POST {draw_id, shared_type, password}
    """
    draw_id = request.GET.get('draw_id')
    password = request.GET.get('password')
    new_password = request.GET.get('new_password')
    shared_type = request.GET.get('shared_type')
    enable_chat = request.GET.get('enable_chat') == "true"
    show_in_public_list = request.GET.get('show_in_public_list') == "true"

    if shared_type not in ("Public", "Invite", None):
        LOG.warning("Wrong type of public draw: {0}".format(shared_type))
        return HttpResponseBadRequest()
    if draw_id is None:
        LOG.warning("Empty draw_id")
        return HttpResponseBadRequest()
    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw) # raises 500

    if shared_type == "Public":
        bom_draw.shared_type = shared_type
        bom_draw.password = new_password
        bom_draw.show_in_public_list = show_in_public_list
        bom_draw.enable_chat = enable_chat
    elif shared_type == "Invite":
        bom_draw.shared_type = shared_type
        bom_draw.password = None
        bom_draw.show_in_public_list = show_in_public_list
        bom_draw.enable_chat = enable_chat
    elif shared_type is None:
        bom_draw.shared_type = shared_type
        bom_draw.password = None
        bom_draw.show_in_public_list = False
        bom_draw.enable_chat = False

    MONGO.save_draw(bom_draw)
    LOG.info("Draw {0} updated to {1}".format(
        bom_draw.pk, bom_draw.share_settings))
    return HttpResponse()


