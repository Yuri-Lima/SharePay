
from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url, reverse
from .models import CustomUser


class CustomUserSitemap(Sitemap):
    changefreq = "hourly"

    def items(self):
        return ['users:signup', 'users:login', 'users:logout']

    def location(self, item):
        return reverse(item)
