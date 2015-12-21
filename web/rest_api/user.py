import json

from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from tastypie import fields, resources, exceptions, http
from tastypie.utils import trailing_slash
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
        extra_actions = [
            {
                "name": "login",
                "http_method": "POST",
                "resource_type": "list",
                "description": "Authenticate user",
            },
            {
                "name": "logout",
                "http_method": "POST",
                "resource_type": "list",
                "description": "Logout user",
            },
        ]

    @property
    def _client(self):
        return mongodb.MongoDriver.instance()

    def prepend_urls(self):
        return [
            url(r"^%s/login%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('user_login'),
                name="api_login"),
            url(r"^%s/logout%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('user_logout'),
                name="api_logout"),
        ]

    def user_login(self, request, **_):
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        try:
            data = json.loads(request.body)
        except TypeError:
            data = json.loads(request.body.decode('utf-8'))

        email = data.pop('email')
        password = data.pop('password')

        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                if 'keep-logged' in request.POST:
                    request.session.set_expiry(31556926)  # 1 year
                login(request, user)
                return self.create_response(request, "User authenticated")
            else:
                raise exceptions.ImmediateHttpResponse(
                    response=http.HttpUnauthorized("The user is not ativated"))
        else:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpUnauthorized("Incorrect credentials"))

    def user_logout(self, request, **_):
        self.method_check(request, allowed=['post'])
        logout(request)
        return self.create_response(request, "User logged out")

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
        try:
            user = self._client.retrieve_user(kwargs['pk'])
        except mongodb.MongoDriver.NotFoundError:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpNotFound())
        else:
            return user

    def obj_create(self, bundle, **kwargs):
        bundle.obj = bom.User(_id=bundle.data["email"])
        bundle.obj.set_password(bundle.data["password"])
        try:
            self._client.create_user(bundle.obj)
        except mongodb.MongoDriver.UserExistsError as e:
            raise exceptions.ImmediateHttpResponse(response=http.HttpConflict(e))
        return bundle

    def obj_update(self, bundle, **kwargs):
        if bundle.obj.pk != bundle.request.user.pk:
            raise exceptions.ImmediateHttpResponse(
                response=http.HttpUnauthorized("An user can only update "
                                               "his own details"))

        for key, value in bundle.data.items():
            if key in self.FROZEN_ATTRIBUTES:
                if getattr(bundle.obj, key, value) != value:
                    raise exceptions.ImmediateHttpResponse(
                        response=http.HttpBadRequest(
                            "Invalid attribute {0}".format(key)))
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
