from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#Google Robots >> robots.txt <<
from django.views.generic import TemplateView
# Sitemap from django
from django.contrib.sitemaps.views import sitemap
#Sitemaps from apps
from share.sitemaps import (
    HouseNameSitemap,
    HouseTenantSitemap,
    HouseKilowattSitemap,
    HouseBillSitemap,
    SubHouseNameSitemap,
    SubKilowattSitemap,
    SubTenantSitemap, 
)
from users.sitemaps import CustomUserSitemap
#Dict Sitemaps
# https://www.youtube.com/watch?v=xAXMqiPSY34
sitemaps = {
    'housename': HouseNameSitemap,
    'housetenant': HouseTenantSitemap,
    'Housekilowatts': HouseKilowattSitemap,
    'housebill': HouseBillSitemap,
    'subhousename' : SubHouseNameSitemap,
    'subkilowatts' : SubKilowattSitemap,
    'subtenant' : SubTenantSitemap,
    'users' : CustomUserSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),

    #Share URLS
    path('', include('share.urls')),

    #SiteMap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    #Google Robots >> robots.txt << https://developers.google.com/search/docs/advanced/robots/create-robots-txt?hl=en
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]
#Static Paths >> static <<
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Error Pages Paths >> ERROR PAGES <<
handler404 = 'share.views.handle_page_not_found_404'
handler500 = 'share.views.handle_server_error_500'
handler403 = 'share.views.handle_permission_denied_403'
handler400 = 'share.views.handle_bad_request_400' 
