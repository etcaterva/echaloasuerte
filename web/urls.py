from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from web import views

urlpatterns = patterns(None)

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^number.html$', views.random_number_draw, name="random_number"),
    url(r'^item.html$', views.random_item_draw, name="random_item"),
    url(r'^link_sets.html$', views.link_sets_draw, name="link_sets"),
    url(r'^coin.html$', views.coin_draw, name="coin"),
    url(r'^card.html$', views.card_draw, name="card"),
    url(r'^dice_new.html$', views.dice_draw, name="dice"),
    url(r'^about.html$', views.under_construction, name="about"),
    url(r'^joinpublicdraw.html$', views.under_construction, name="join_public_draw"),
    url(r'^publishdraw.html$', views.under_construction, name="publish_draw"),
    url(r'^draw/(?P<draw_id>[0-9a-g]+)/$', views.retrieve_draw, name="retrieve_draw"),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/forgot_password/$', views.under_construction, name='forgot_password'),
    url(r'^accounts/login/$', views.login_user, name='login'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
)
