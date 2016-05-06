from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from web import views
from web import web_services as ws


urlpatterns = patterns(None)

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^about.html$', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/$', views.display_draw, name="retrieve_draw"),
    url(r'^draw/new/(?P<draw_type>[^/]+)/public/$', views.create_draw, {'is_public': True},
        name="create_public_draw"),
    url(r'^draw/new/(?P<draw_type>[^/]+)/$', views.create_draw, {'is_public': False},
        name="create_draw"),
    url(r'^registration_success/$', TemplateView.as_view(template_name='registration_success.html'),
        name='registration_success'),
    url(r'^accounts/register/$', TemplateView.as_view(template_name='register.html'), name='register'),
    url(r'^accounts/forgot_password/$', views.under_construction, name='forgot_password'),
    url(r'^accounts/login/$', TemplateView.as_view(template_name='login.html'), name='login'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^join_draw.html$', views.join_draw, name="join_public_draw"),
    url(r'^pusher/auth$', views.pusher_authenticate, name="pusher_auth"),
)

# web services
urlpatterns += patterns(
    '',
    url(r'^ws/feedback/$', ws.feedback, name="ws_feedback"),
)

# service workers
urlpatterns += patterns(
    'django.contrib.staticfiles.views',
    url(r'^service-worker\.js$', 'serve', kwargs={'path': 'js/sw.js'})
)

urlpatterns += staticfiles_urlpatterns()
