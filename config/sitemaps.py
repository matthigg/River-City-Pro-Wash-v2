from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'contact', 'faq', 'our-work', 'services', 'house-washing', 'concrete-brick-washing', 'deck-patio-washing', 'deck-staining', 'fence-cleaning', 'graffiti-removal']

    def location(self, item):
        return reverse(item)