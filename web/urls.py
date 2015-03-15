from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from web import views

urlpatterns = patterns(None)

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name='index'),

    url(r'^draw/(?P<draw_type>[a-zA-Z_]+)/(?P<publish>publish)?$', views.draw, name="draw"),
    url(r'^draw/(?P<draw_type>[a-zA-Z_]+)/(?P<draw_id>[0-9a-g]+)?$', views.draw, name="draw"),

    url(r'^publish_draw.html$', views.index, {'is_public': True}, name="publish_draw"),
    url(r'^join_draw.html$', views.join_draw, name="join_public_draw"),

    url(r'^about.html$', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/$', views.retrieve_draw, name="retrieve_draw"),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/forgot_password/$', views.under_construction, name='forgot_password'),
    url(r'^accounts/login/$', views.login_user, name='login'),
    url(r'^accounts/profile/$', views.profile, name='profile'),

    #web services
    url(r'^ws/draw_add_users/$', views.add_user_to_draw, name="ws_add_users_to_draw"),
    url(r'^ws/favourites/add/$', views.add_favorite, name="ws_add_favorite"),
    url(r'^ws/favourites/remove/$', views.remove_favorite, name="ws_remove_favorite"),
)
