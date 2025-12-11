from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),  # root redirects to /events/
] + debug_toolbar_urls()



