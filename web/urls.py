from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from web import views
from web import web_services as ws


urlpatterns = patterns(None)

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^about.html$', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/$', views.display_draw, name="retrieve_draw"),
    url(r'^draw/new/(?P<draw_type>[^/]+)/shared/$', views.create_draw, {'is_shared': True},
        name="create_shared_draw"),
    url(r'^draw/new/(?P<draw_type>[^/]+)/$', views.create_draw, {'is_shared': False},
        name="create_draw"),
    url(r'^registration_success/$', TemplateView.as_view(template_name='registration_success.html'),
        name='registration_success'),
    url(r'^accounts/register/$', TemplateView.as_view(template_name='register.html'), name='register'),
    url(r'^accounts/forgot_password/$', views.reset, name='forgot_password'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset_success/$', TemplateView.as_view(template_name='reset_success.html'), name='reset_success'),
    url(r'^accounts/login/$', TemplateView.as_view(template_name='login.html'), name='login'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^join_draw.html$', views.join_draw, name="join_shared_draw"),
    url(r'^pusher/auth$', views.pusher_authenticate, name="pusher_auth"),
    url(r'^service\-worker\.js$', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'))
)

# web services
urlpatterns += patterns(
    '',
    url(r'^ws/feedback/$', ws.feedback, name="ws_feedback"),
)

urlpatterns += staticfiles_urlpatterns()
