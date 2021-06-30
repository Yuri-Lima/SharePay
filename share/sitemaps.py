
from django.contrib.sitemaps import Sitemap
from django.urls.base import reverse
from .models import (
    HouseNameModel,
    HouseBillModel,
    HouseKilowattModel,
    HouseTenantModel,
    SubHouseNameModel,
    SubKilowattModel,
    SubTenantModel,
    )

class IndexSiteamp(Sitemap):
    changefreq = 'weekly'
    
    def items(self):
        return ['share:index']

    def location(self, item):
        return reverse(item)


class HouseNameSitemap(Sitemap):
    changefreq = "hourly"

    # def items(self):
    #     return HouseNameModel.objects.all()

    # def lastmod(self, obj):
    #     return obj.last_updated_house

class HouseBillSitemap(Sitemap):
    changefreq = "hourly"

    # def items(self):
    #     return HouseBillModel.objects.all()

    # def lastmod(self, obj):
    #     return obj.last_updated_bill

class HouseKilowattSitemap(Sitemap):
    changefreq = "hourly"

    # def items(self):
    #     return HouseKilowattModel.objects.all()

    # def lastmod(self, obj):
    #     return obj.last_updated_kwh

class HouseTenantSitemap(Sitemap):
    changefreq = "hourly"

    # def items(self):
    #     return HouseTenantModel.objects.all()

    # def lastmod(self, obj):
    #     return obj.last_updated_tenant

class SubHouseNameSitemap(Sitemap):
    changefreq = "hourly"

    # def items(self):
    #     self.add = list()
    #     for obj in HouseNameModel.objects.all():
    #         for sub_obj in SubHouseNameModel.objects.filter(pk=obj.pk):
    #             self.add.append(sub_obj)
    #             print(self.add)
    #     return self.add

    # def location(self, obj):
    #     return reverse([a for a in self.add])

class SubKilowattSitemap(Sitemap):
    changefreq = "hourly"

    # def items(self):
    #     return SubKilowattModel.objects.all()

    # def lastmod(self, obj):
    #     return obj.sub_last_updated_kwh

class SubTenantSitemap(Sitemap):
    changefreq = "hourly"

    # def items(self):
    #     return SubTenantModel.objects.all()

    # def lastmod(self, obj):
    #     return obj.sub_last_updated_tenant