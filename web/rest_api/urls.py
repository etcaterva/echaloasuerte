from django.conf.urls import patterns, include, url
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
    url(r'doc/',
        include('tastypie_swagger.urls', namespace='api_doc'),
        kwargs={
            "tastypie_api_module": v1_api,
            "namespace": "api_doc",
            "version": "1.0"}
        ),
)
