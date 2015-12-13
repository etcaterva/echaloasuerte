from calendar import timegm
from django.contrib import sitemaps
import datetime
from django.contrib.sitemaps.views import x_robots_tag
from django.contrib.sites.models import Site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.http import http_date
from django.utils import six
from server.draw_factory import REGISTRY


class LandingSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.9
    lastmod = datetime.datetime.now()

    def items(self):
        return ['index']

    def location(self, obj):
        return reverse(obj)


class DrawSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8
    lastmod = datetime.datetime.now()

    def items(self):
        return [draw_meta['form'].NAME_IN_URL for draw_meta in REGISTRY.values()]

    def location(self, obj):
        return reverse('create_draw', args=[obj])


class OthersSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.6
    lastmod = datetime.datetime.now()

    def items(self):
        return ['about']

    def location(self, obj):
        return reverse(obj)

#
# @x_robots_tag
# def sitemap(request, sitemaps, template_name='sitemap.xml', content_type='application/xml'):
#     req_protocol = request.scheme
#     host = request.META.get('HTTP_HOST')
#     req_site = Site(domain=host)
#
#     maps = list(six.itervalues(sitemaps))
#     page = request.GET.get("p", 1)
#
#     urls = []
#     for site in maps:
#         try:
#             if callable(site):
#                 site = site()
#             urls.extend(site.get_urls(page=page, site=req_site,
#                                       protocol=req_protocol))
#         except EmptyPage:
#             raise Http404("Page %s empty" % page)
#         except PageNotAnInteger:
#             raise Http404("No page '%s'" % page)
#     response = TemplateResponse(request, template_name, {'urlset': urls},
#                                 content_type=content_type)
#     if hasattr(site, 'latest_lastmod'):
#         # if latest_lastmod is defined for site, set header so as
#         # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
#         response['Last-Modified'] = http_date(
#             timegm(site.latest_lastmod.utctimetuple()))
#     return response
