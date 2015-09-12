from django.conf.urls import patterns, include
from tastypie.api import Api

from web.rest_api.draw import DrawResource
from web.rest_api.user import UserResource
from web.rest_api.favourite import FavouriteResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(FavouriteResource())
v1_api.register(DrawResource())

urlpatterns = patterns(
    '',
    (r'^', include(v1_api.urls)),
)
