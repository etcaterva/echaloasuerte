from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from web import views

urlpatterns = patterns(None)

urlpatterns += patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^number.html$', views.random_number_draw, name="random_number"),
    url(r'^item.html$', views.random_item_draw, name="random_item"),

)
