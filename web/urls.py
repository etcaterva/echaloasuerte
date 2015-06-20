from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from web import views
from web import web_services as ws
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns(None)

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name='index'),

    url(r'^publish_draw.html$', views.index, {'is_public': True}, name="publish_draw"),
    url(r'^join_draw.html$', views.join_draw, name="join_public_draw"),

    url(r'^about.html$', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/$', views.display_draw, name="retrieve_draw"),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/update/$', views.update_draw, name="update_draw"),
    url(r'^draw/new/(?P<draw_type>[^/]+)/public/$', views.create_draw, {'is_public': True}, name="create_public_draw"),
    url(r'^draw/new/(?P<draw_type>[^/]+)/$', views.create_draw, {'is_public': False}, name="create_draw"),
    url(r'^draw/try/(?P<draw_type>[^/]+)/$', views.try_draw, name="try_draw"),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/forgot_password/$', views.under_construction, name='forgot_password'),
    url(r'^accounts/login/$', views.login_user, name='login'),
    url(r'^accounts/profile/$', views.profile, name='profile'),

    #web services
    url(r'^ws/draw/toss/$', ws.toss_draw, name="ws_toss_draw"),
    url(r'^ws/draw/try/$', ws.try_draw, name="ws_try_draw"),
    url(r'^ws/draw/validate/$', ws.validate_draw, name="ws_validate_draw"),
    url(r'^ws/draw/share_settings/update/$', ws.update_share_settings, name="ws_update_share_settings"),
    url(r'^ws/chat/details/$', ws.get_draw_details, name="ws_get_draw_details"),
    url(r'^ws/favourites/add/$', ws.add_favorite, name="ws_add_favorite"),
    url(r'^ws/chat/add/$', ws.add_message_to_chat, name="chat_add_message"),

    url(r'^ws/draw_add_users/$', ws.add_user_to_draw, name="ws_add_users_to_draw"),
    url(r'^ws/favourites/remove/$', ws.remove_favorite, name="ws_remove_favorite"),
    url(r'^ws/check_access_to_draw/$', ws.check_access_to_draw, name="check_access_to_draw"),
)

urlpatterns += staticfiles_urlpatterns()
