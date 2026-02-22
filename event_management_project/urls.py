from django.contrib import admin
from django.urls import path, include
#from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home_page, no_permission
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', organizer_dashboard, name='home'),
    path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('no-permission/', no_permission, name='no-permission')
]
#+ debug_toolbar_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)