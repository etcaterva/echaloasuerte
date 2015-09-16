from tastypie import fields, resources, exceptions
from tastypie.bundle import Bundle

from server import bom, mongodb


class UserResource(resources.Resource):
    """Echaloasuerte user.

    Allows to create users and update some of its fields.
    """
    email = fields.CharField(attribute='_id',
                             help_text="Email of the user")
    alias = fields.CharField(attribute='alias',
                             help_text="Alias to be displayed")
    use_gravatar = fields.BooleanField(attribute='use_gravatar', default=False,
                                       help_text="Whether to use the user's "
                                                 "email gravatar or a random "
                                                 "monster as user's picture")

    FROZEN_ATTRIBUTES = ['resource_uri', 'email', '_id']
    """Attributes that cannot be updated"""

    class Meta:
        resource_name = 'user'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'patch']

    @property
    def _client(self):
        return mongodb.MongoDriver.instance()

    def detail_uri_kwargs(self, bundle_or_obj):
        if isinstance(bundle_or_obj, Bundle):
            return {'pk': bundle_or_obj.obj.pk}
        else:
            return {'pk': bundle_or_obj.pk}

    def get_object_list(self, request):
        result = []
        if request.user.is_authenticated():
            result.append(self._client.retrieve_user(request.user.pk))
        return result

    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for the moment
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        user = self._client.retrieve_user(kwargs['pk'])
        return user

    def obj_create(self, bundle, **kwargs):
        bundle.obj = bom.User(_id=bundle.data["email"])
        bundle.obj.set_password(bundle.data["password"])
        self._client.save_user(bundle.obj)
        return bundle

    def obj_update(self, bundle, **kwargs):
        if bundle.obj.pk != bundle.request.user.pk:
            self.unauthorized_result(None)

        for key, value in bundle.data.items():
            if key in self.FROZEN_ATTRIBUTES:
                if getattr(bundle.obj, key, value) != value:
                    raise exceptions.BadRequest()
            elif key == 'password':
                bundle.obj.set_password(bundle.data['password'])
            else:
                setattr(bundle.obj, key, value)

        self._client.save_user(bundle.obj)
        return bundle

    def obj_delete(self, bundle, **kwargs):
        self._client.remove_user(bundle.obj.pk)

    def rollback(self, bundles):
        pass