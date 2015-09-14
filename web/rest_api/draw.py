from tastypie import fields, resources, http, exceptions
from tastypie.bundle import Bundle

from server import mongodb, draw_factory


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

    class Meta:
        resource_name = 'draw'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'delete']

    @property
    def _client(self):
        return mongodb.MongoDriver.instance()

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
        if 'type' not in data:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Missing draw type"))
        type_ = data.pop('type')

        for attr in self.FORBIDDEN_ATTRIBUTES:
            if attr in data:
                raise exceptions.ImmediateHttpResponse(
                    response=http.HttpBadRequest("{0} is forbidden".format(
                        attr)))

        draw = draw_factory.create_draw(type_, data)
        draw.owner = bundle.request.user.pk
        if not draw.is_feasible():
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpBadRequest("Not feasible"))
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