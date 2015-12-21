import datetime

from django.contrib import sitemaps
from django.core.urlresolvers import reverse

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
