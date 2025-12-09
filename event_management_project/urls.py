from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('', RedirectView.as_view(url='/events/', permanent=True)),  # root redirects to /events/
] + debug_toolbar_urls()



