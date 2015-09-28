"""definition of basic web services"""
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.core.validators import validate_email
from server import draw_factory
from server.mongodb.driver import MongoDriver
from web.common import user_can_read_draw, user_can_write_draw, time_it, invite_user, \
    set_owner, ga_track_draw
from server.forms import *
from server.bom import *
import dateutil.parser

LOG = logging.getLogger("echaloasuerte")
MONGO = MongoDriver.instance()


@login_required
@time_it
def update_user(request):
    """updates the details of a user"""
    # DEPRECATE
    user = MONGO.retrieve_user(request.user.pk)
    result = "ko"

    if "email" in request.POST:
        pass  # user._id = request.POST["email"]
    if "new_password" in request.POST:
        if "current_password" in request.POST and user.check_password(request.POST["current_password"]):
            user.set_password(request.POST["new_password"])
            result = "ok"
    if "alias" in request.POST:
        user.alias = request.POST["alias"]
        result = "ok"
    if "use_gravatar" in request.POST:
        user.use_gravatar= request.POST["use_gravatar"] == "true"
        result = "ok"
    MONGO.save_user(user)
    return HttpResponse(result)


@time_it
def feedback(request):
    """sends the feedback data to the users"""
    type_ = request.POST.get("type")
    comment = request.POST.get("comment")
    email = request.POST.get("email", "anonymous")
    browser = request.POST.get("browser", "Unknown Browser")
    subject = """Feedback ({0})""".format(type_)
    message = """{0}\nBy {1} on {2}""".format(comment,
                                              email,
                                              browser)
    if type_ and comment:
        mail_admins(subject, message, True)
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Invalid feedback, type or comment missing")


@time_it
def toss_draw(request):
    """generates a result and returns it"""
    # DEPRECATE
    draw_id = request.GET.get("draw_id")
    if draw_id is None:
        return HttpResponseBadRequest()
    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)  # raises 500
    result = bom_draw.toss()
    MONGO.save_draw(bom_draw)
    ga_track_draw(bom_draw, "toss")
    return JsonResponse({
        "result": result
    })

@time_it
def schedule_toss_draw(request):
    """generates a result and returns it"""
    # DEPRECATE
    draw_id = request.GET.get("draw_id")
    schedule = request.GET.get("schedule")
    if draw_id is None or schedule is None:
        return HttpResponseBadRequest()
    schedule = dateutil.parser.parse(schedule)
    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)  # raises 500
    result = bom_draw.timed_toss(schedule)
    MONGO.save_draw(bom_draw)
    return JsonResponse({
        "result": result
    })


@time_it
def try_draw(request, draw_id):
    """generates a result and returns it"""
    # DEPRECATE
    bom_draw = MONGO.retrieve_draw(draw_id)
    return JsonResponse({
        "result": bom_draw.toss()
    })


@login_required
@time_it
def add_user_to_draw(request):
    """Add an user to a draw and sends a mail to inform him"""
    # DEPRECATE
    draw_id = request.GET.get('draw_id')
    users_to_add = request.GET.get('emails', "")

    if draw_id is None:
        return HttpResponseBadRequest()

    LOG.info("Adding {0} to draw {1}".format(users_to_add, draw_id))
    bom_draw = MONGO.retrieve_draw(draw_id)

    user_can_write_draw(request.user, bom_draw)  # Raises 500

    new_users = users_to_add.replace(',', ' ').split()

    try:
        for email in new_users:
            validate_email(email)  # Raises a ValidationError
    except ValidationError:
        LOG.info("One or more emails are not correct")
        return HttpResponseBadRequest()

    bom_draw.users += new_users
    MONGO.save_draw(bom_draw)

    invite_user(new_users, draw_id, request.user.email)

    LOG.info("{0} users added to draw {1}".format(len(new_users), draw_id))

    return HttpResponse()


@login_required
@time_it
def remove_user_from_draw(request):
    """Remove an user from a draw"""
    # DEPRECATE
    draw_id = request.GET.get('draw_id')
    users = request.GET.get('emails', "")

    if draw_id is None:
        return HttpResponseBadRequest()

    LOG.info("Removing {0} from draw {1}".format(users, draw_id))
    bom_draw = MONGO.retrieve_draw(draw_id)

    user_can_write_draw(request.user, bom_draw)  # Raises 500

    remove_users = users.replace(',', ' ').split()
    bom_draw.users = [email for email in bom_draw.users
                      if email not in remove_users]
    MONGO.save_draw(bom_draw)

    return HttpResponse()


@login_required
@time_it
def add_favorite(request):
    """Add a draw to the list of favourites of an user"""
    # DEPRECATE
    draw_id = request.GET.get('draw_id')

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)  # raises 500
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
    # DEPRECATE
    draw_id = request.GET.get('draw_id')

    if draw_id is None:
        return HttpResponseBadRequest()

    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)  # raises 500
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
    # is this used?
    draw_id = request.GET.get('draw_id')
    draw = MONGO.retrieve_draw(draw_id)

    user_can_read_draw(request.user, draw)
    return HttpResponse()


def add_message_to_chat(request):
    """Adds a message to a chat"""
    draw_id = request.GET.get('draw_id')
    message = request.GET.get('message')
    user = request.GET.get('user_name')
    MONGO.add_chat_message(draw_id, message, user)
    return HttpResponse()


# @time_it
def get_draw_details(request):
    def get_user_image(username):
        """function to get either the user avatar or an empty string"""
        try:
            return MONGO.retrieve_user(username).user_image
        except Exception:
            return ""
    draw_id = request.GET.get('draw_id')
    draw = MONGO.retrieve_draw(draw_id)
    try:
        messages = MONGO.retrieve_chat_messages(draw_id)
    except MongoDriver.NotFoundError:
        messages = []

    try:
        users = set([message["user"] for message in messages])
        users_map = {name: get_user_image(name) for name in users}
        for message in messages:
            message["avatar"] = users_map[message["user"]]
    except Exception as exception:
        LOG.exception(exception)

    return JsonResponse({
        "messages": messages,
        "enable_chat": draw.enable_chat,
        "last_updated_time": draw.last_updated_time
    })


@time_it
def validate_draw(request):
    """WS to validate a draw"""
    draw_type = request.POST.get("draw_type")
    if not draw_type:
        return HttpResponseBadRequest("Missing post argument draw_type")

    logger.debug("Received post data: {0}".format(request.POST))
    draw_form = draw_factory.create_form(draw_type, data=request.POST)
    try:
        _ = draw_form.build_draw()
    except DrawFormError:
        logger.info("Form not valid: {0}".format(draw_form.errors))
        return JsonResponse({
            "is_valid": False,
            "errors": draw_form.errors
        })
    else:
        return JsonResponse({
            "is_valid": True,
        })


@time_it
def update_share_settings(request):
    """Updates the shared settings.

    input POST {draw_id, enable_chat}
    """
    # DEPRECATE
    draw_id = request.GET.get('draw_id')
    enable_chat = request.GET.get('enable_chat') == "true"
    if draw_id is None:
        LOG.warning("Empty draw_id")
        return HttpResponseBadRequest()
    bom_draw = MONGO.retrieve_draw(draw_id)
    user_can_write_draw(request.user, bom_draw)  # raises 500
    bom_draw.enable_chat = enable_chat

    MONGO.save_draw(bom_draw)
    LOG.info("Draw {0} updated".format(bom_draw.pk))
    return HttpResponse()

@time_it
def create_draw(request):
    """create_draw ws
    """
    # DEPRECATE
    LOG.debug("Received post data: {0}".format(request.POST))

    draw_type = request.POST.get("draw_type")
    if not draw_type:
        return HttpResponseBadRequest("Missing post argument draw_type")

    draw_form = draw_factory.create_form(draw_type, data=request.POST)
    try:
        bom_draw = draw_form.build_draw()
    except DrawFormError:
        LOG.info("Form not valid: {0}".format(draw_form.errors))
        return HttpResponseBadRequest("Not valid")
    else:
        bom_draw._id = None  # Ensure we have no id
        set_owner(bom_draw, request)
        MONGO.save_draw(bom_draw)
        LOG.info("Generated draw: {0}".format(bom_draw))
        ga_track_draw(bom_draw, "create_draw")
        #  notify users if any
        if bom_draw.users:
            invite_user(bom_draw.users, bom_draw.pk, bom_draw.owner)
        draw_url = reverse('retrieve_draw', args=(bom_draw.pk, ))
        return JsonResponse({'draw_url': draw_url})
