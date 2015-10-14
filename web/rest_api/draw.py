import json
import pytz
from tastypie import fields, resources, http, exceptions
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
from django.conf.urls import url
import dateutil.parser

from server import mongodb, draw_factory, bom


class DrawResource(resources.Resource):
    """Generic resource for draws.

    Post and delete to a draw with id to add or remove yourself from the users
    involved in the draw.
    GET on the resource returns all draws you are linked with. Either as a owner
    or as an user.
    """
    id = fields.CharField(attribute='_id', help_text="id of the favourite draw")
    type = fields.CharField(attribute='draw_type', help_text="type of the draw")
    title = fields.CharField(attribute='title',
                             help_text="Title of the draw",
                             null=True)
    description = fields.CharField(attribute='description',
                                   help_text="Description of the draw",
                                   null=True)
    is_shared = fields.BooleanField(attribute='is_shared',
                                    default=False,
                                    help_text="Whether the draw is public or not")
    owner = fields.CharField(attribute='owner',
                             null=True,
                             help_text="Owner of the draw")
    number_of_results = fields.IntegerField(attribute='number_of_results',
                                            default=1,
                                            help_text='Number of results to'
                                                      ' generate when tossing')

    HIDDEN_ATTRIBUTES = ['draw_type', '_id']
    FORBIDDEN_ATTRIBUTES = ['results', 'owner', '_id', 'pk', 'creation_time',
                            'last_updated_time', 'audit']
    FROZEN_ATTRIBUTES = ['type']

    class Meta:
        resource_name = 'draw'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'delete', 'patch']
        extra_actions = [
            {
                "name": "toss",
                "http_method": "POST",
                "resource_type": "detail",
                "description": "Toss a draw",
            },
            {
                "name": "try",
                "http_method": "POST",
                "resource_type": "list",
                "description": "Toss without saving a draw"
            },
            {
                "name": "schedule_toss",
                "http_method": "POST",
                "resource_type": "detail",
                "description": "Schedules a toss"
            },
            {
                "name": "chat",
                "http_method": "POST",
                "resource_type": "detail",
                "description": "Add chat entry",
            },
            {
                "name": "chat",
                "http_method": "GET",
                "resource_type": "detail",
                "description": "Retrieve chat entries",
            },
        ]

    @property
    def _client(self):
        return mongodb.MongoDriver.instance()

    def prepend_urls(self):
        return [
            url(r"^%s/(?P<pk>.*?)/toss%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('toss'),
                name="api_draw_toss"),
            url(r"^%s/try%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('try_draw'),
                name="api_draw_try"),
            url(r"^%s/(?P<pk>.*?)/schedule_toss/(?P<schedule>.*?)%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('schedule_toss'),
                name="api_draw_schedule"),
            url(r"^%s/(?P<pk>.*?)/chat%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('chat'),
                name="api_draw_chat"),
        ]

    def chat(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'get'])
        self.throttle_check(request)
        draw_id = kwargs['pk']
        try:
            draw = self._client.retrieve_draw(draw_id)  # check exists
        except mongodb.MongoDriver.NotFoundError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpNotFound())
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except TypeError:
                data = json.loads(request.body.decode('utf-8'))
            try:
                message = data['message']
                user = data['user']
                self._client.add_chat_message(draw_id, message, user)
            except KeyError:
                raise exceptions.ImmediateHttpResponse(
                    response=http.HttpBadRequest("Missing message or username"))
            return self.create_response(request, {})
        elif request.method == 'GET':
            # TODO: return only the list of messages
            def get_user_image(username):
                """function to get either the user avatar or an empty string"""
                try:
                    return self._client.retrieve_user(username).user_image
                except Exception:
                    return ""
            try:
                messages = self._client.retrieve_chat_messages(draw_id)
            except mongodb.MongoDriver.NotFoundError:
                messages = []

            users = set([message["user"] for message in messages])
            users_map = {name: get_user_image(name) for name in users}
            for message in messages:
                message["avatar"] = users_map[message["user"]]

            return self.create_response(request, {
                "messages": messages,
                "enable_chat": draw.enable_chat,
                "last_updated_time": draw.last_updated_time
            })

    def toss(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        draw_id = kwargs['pk']
        try:
            bom_draw = self._client.retrieve_draw(draw_id)
        except mongodb.MongoDriver.NotFoundError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpNotFound())
        if not bom_draw.check_write_access(request.user):
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpUnauthorized("Only the owner can toss"))
        result = bom_draw.toss()
        self._client.save_draw(bom_draw)
        self.log_throttled_access(request)
        return self.create_response(request, result)

    def try_draw(self, request, **_):
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        try:
            data = json.loads(request.body)
        except TypeError:
            data = json.loads(request.body.decode('utf-8'))

        try:
            type_ = data.pop('type')
            draw = draw_factory.create_draw(type_, data)
            draw.validate()
        except KeyError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Missing draw type"))
        except draw_factory.DrawNotRegistered:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Invalid draw type"))
        except bom.InvalidDraw as e:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest(e.serialize()))
        self._client.save_draw(draw)
        result = draw.toss()
        self.log_throttled_access(request)
        return self.create_response(request, result)

    def schedule_toss(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        draw_id = kwargs['pk']
        try:
            schedule = kwargs['schedule']
            schedule = dateutil.parser.parse(schedule).astimezone(pytz.utc)
            bom_draw = self._client.retrieve_draw(draw_id)
        except (ValueError, KeyError):
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Invalid 'schedule'"))
        except mongodb.MongoDriver.NotFoundError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpNotFound())
        if not bom_draw.check_write_access(request.user):
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpUnauthorized(
                    "Only the owner can schedule a toss"))
        result = bom_draw.timed_toss(schedule)
        self._client.save_draw(bom_draw)
        self.log_throttled_access(request)
        return self.create_response(request, result)

    def dehydrate(self, bundle):
        bundle.data["users"] = bundle.obj.users
        for att in bundle.obj.__dict__:
            if att not in bundle.data:
                bundle.data[att] = getattr(bundle.obj, att)
        for att in self.HIDDEN_ATTRIBUTES:
            bundle.data.pop(att)
        bundle.data["type"] = draw_factory.get_draw_name(bundle.data["type"])
        return bundle

    def detail_uri_kwargs(self, bundle_or_obj):
        if isinstance(bundle_or_obj, Bundle):
            return {'pk': bundle_or_obj.obj.pk}
        else:
            return {'pk': bundle_or_obj.pk}

    def get_object_list(self, request):
        result = []
        if request.user.is_authenticated():
            draws = self._client.get_draws_with_filter({
                '$or': [
                    {'owner': request.user.pk},
                    {'users': request.user.pk},
                ]
            })
            result.extend(draws)
        return result

    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for the moment
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        try:
            return self._client.retrieve_draw(kwargs['pk'])
        except mongodb.MongoDriver.NotFoundError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpNotFound())

    def obj_create(self, bundle, **kwargs):
        data = bundle.data
        for attr in self.FORBIDDEN_ATTRIBUTES:
            if attr in data:
                raise exceptions.ImmediateHttpResponse(
                    response=http.HttpBadRequest("{0} is forbidden".format(
                        attr)))
        try:
            type_ = data.pop('type')
            draw = draw_factory.create_draw(type_, data)
            draw.validate()
        except KeyError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Missing draw type"))
        except draw_factory.DrawNotRegistered:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Invalid draw type"))
        except bom.InvalidDraw as e:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest(e.serialize()))
        draw.owner = bundle.request.user.pk
        self._client.save_draw(draw)
        bundle.obj = draw
        return bundle

    def obj_update(self, bundle, **kwargs):
        draw_id = kwargs['pk']
        try:
            draw = self._client.retrieve_draw(draw_id)
        except mongodb.MongoDriver.NotFoundError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Draw not found"))
        if not draw.check_write_access(bundle.request.user):
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpUnauthorized("Only the owner can update"))

        for name, value in bundle.data.items():
            if not hasattr(draw, name):
                continue
            elif name in self.FROZEN_ATTRIBUTES + self.FORBIDDEN_ATTRIBUTES:
                if getattr(draw, name) != value:
                    raise exceptions.ImmediateHttpResponse(
                        response=http.HttpBadRequest("{0} is forbidden".format(
                            name)))
            else:
                setattr(draw, name, value)

        try:
            draw.validate()
        except bom.InvalidDraw as e:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest(e.serialize()))

        draw.add_audit("DRAW_PARAMETERS")
        self._client.save_draw(draw)
        bundle.obj = draw
        return bundle

    def post_detail(self, request, **kwargs):
        if not request.user.is_authenticated():
            self.unauthorized_result(None)
        draw_id = kwargs['pk']
        try:
            draw = self._client.retrieve_draw(draw_id)
        except mongodb.MongoDriver.NotFoundError:
            return http.HttpBadRequest("Draw not found")
        if request.user.pk not in draw.users:
            draw.users.append(request.user.pk)
            self._client.save_draw(draw)
        return http.HttpCreated()

    def obj_delete(self, bundle, **kwargs):
        if not bundle.request.user.is_authenticated():
            self.unauthorized_result(None)
        draw_id = kwargs['pk']
        try:
            draw = self._client.retrieve_draw(draw_id)
        except mongodb.MongoDriver.NotFoundError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpNotFound())
        if bundle.request.user.pk in draw.users:
            draw.users.remove(bundle.request.user.pk)
            self._client.save_draw(draw)
        elif bundle.request.user.pk == draw.owner:
            draw.owner = None
            self._client.save_draw(draw)

    def rollback(self, bundles):
        pass