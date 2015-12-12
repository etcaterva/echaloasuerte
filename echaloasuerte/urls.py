from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
)

urlpatterns += i18n_patterns(
    '',
    url(r'^', include('web.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^api/', include('web.rest_api.urls'))
)

# deprecated urls
urlpatterns += patterns(
    '',
    url(r'index.php', RedirectView.as_view(url="/", permanent=True)),
    url(r'elegirSalas.php', RedirectView.as_view(url="/", permanent=True)),
    url(r'contacto.php', RedirectView.as_view(url="/", permanent=True)),
    url(r'acerca.php', RedirectView.as_view(url="about.html", permanent=True)),
    url(r'^ws/draw_add_users/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/draw_remove_users/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/chat/details/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/chat/add/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/draw/share_settings/update/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/draw/schedule-toss/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/draw/try/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/draw/validate/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/draw/toss/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/draw/create/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/update/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^draw/try/(?P<draw_type>[^/]+)/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/update_profile/$',  RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/favourites/remove/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/favourites/add/$', RedirectView.as_view(url="/", permanent=True)),
    url(r'^ws/check_access_to_draw/$', RedirectView.as_view(url="/", permanent=True)),
)
