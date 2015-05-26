from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from web import views
from web import web_services as ws
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns(None)

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name='index'),

    url(r'^draw/(?P<draw_type>[a-zA-Z_]+)/(?P<publish>publish)?$', views.draw, name="draw"),
    url(r'^draw/(?P<draw_type>[a-zA-Z_]+)/(?P<draw_id>[0-9a-g]+)?$', views.draw, name="draw"),

    url(r'^publish_draw.html$', views.index, {'is_public': True}, name="publish_draw"),
    url(r'^join_draw.html$', views.join_draw, name="join_public_draw"),

    url(r'^about.html$', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/$', views.display_draw, name="retrieve_draw"),
    url(r'^draw/new/(?P<draw_type>[^/]+)/(?P<is_public>[a-zA-Z]+)/$', views.create_draw, name="create_draw"),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/forgot_password/$', views.under_construction, name='forgot_password'),
    url(r'^accounts/login/$', views.login_user, name='login'),
    url(r'^accounts/profile/$', views.profile, name='profile'),

    #web services
    url(r'^ws/draw/toss/$', ws.toss_draw, name="ws_toss_draw"),
    url(r'^ws/draw/try/$', ws.try_draw, name="ws_try_draw"),
    url(r'^ws/draw/share_settings/update/$', ws.try_draw, name="ws_update_share_settings"),

    url(r'^ws/draw_add_users/$', ws.add_user_to_draw, name="ws_add_users_to_draw"),
    url(r'^ws/public_draw_privacy/$', ws.change_privacy_public_draw, name="ws_public_draw_privacy"),
    url(r'^ws/favourites/add/$', ws.add_favorite, name="ws_add_favorite"),
    url(r'^ws/favourites/remove/$', ws.remove_favorite, name="ws_remove_favorite"),
    url(r'^ws/check_access_to_draw/$', ws.check_access_to_draw, name="check_access_to_draw"),
    url(r'^ws/chat/add/$', ws.add_message_to_chat, name="chat_add_message"),
    url(r'^ws/chat/get/$', ws.get_chat_messages, name="chat_get_messages"),
)

urlpatterns += staticfiles_urlpatterns()
