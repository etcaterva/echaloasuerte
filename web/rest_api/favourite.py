from collections import namedtuple
from tastypie import fields, resources
from tastypie.bundle import Bundle
from server import mongodb


FavouriteDraw = namedtuple('FavouriteDraw', 'id type')

class FavouriteResource(resources.Resource):
    """Favourites draws of an user

    Allows to add/remove/retrieve the favourites of an user.
    All operations requires the user to be logged in.
    """
    id = fields.CharField(attribute='id', help_text="id of the favourite draw")
    type = fields.CharField(attribute='type', help_text="type of the draw")

    class Meta:
        resource_name = 'favourite'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['delete']

    @property
    def _client(self):
        return mongodb.MongoDriver.instance()

    def detail_uri_kwargs(self, bundle_or_obj):
        if isinstance(bundle_or_obj, Bundle):
            return {'pk': bundle_or_obj.obj.id}
        else:
            return {'pk': bundle_or_obj.id}

    def get_object_list(self, request):
        result = []
        if request.user.is_authenticated():
            user = self._client.retrieve_user(request.user.pk)
            favourites = user.favourites_list
            result.extend([FavouriteDraw(favourite.pk, favourite.draw_type)
                           for favourite in favourites])
        return result

    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for the moment
        return self.get_object_list(bundle.request)

    def obj_create(self, bundle, **kwargs):
        if not bundle.request.user.is_authenticated():
            self.unauthorized_result(None)
        user = self._client.retrieve_user(bundle.request.user.pk)
        draw_id = bundle.data["id"]
        draw = self._client.retrieve_draw(draw_id)
        bundle.obj = FavouriteDraw(draw_id, draw.draw_type)
        user.favourites.append(draw_id)
        self._client.save_user(user)
        return bundle

    def obj_delete(self, bundle, **kwargs):
        if not bundle.request.user.is_authenticated():
            self.unauthorized_result(None)
        user = self._client.retrieve_user(bundle.request.user.pk)
        draw_id = kwargs['pk']
        if draw_id in user.favourites:
            user.favourites.remove(draw_id)
            self._client.save_user(user)

    def rollback(self, bundles):
        pass