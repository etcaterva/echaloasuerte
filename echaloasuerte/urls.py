from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^i18n/', include('django.conf.urls.i18n')),
                       url(r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += patterns('',
                        url(r'^', include('web.urls')),
                        )
