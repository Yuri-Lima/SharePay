from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    # path('users/', include('django.contrib.auth.urls')),

    #Share URLS
    path('', include('share.urls')),
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
