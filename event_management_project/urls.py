from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect 
#from debug_toolbar.toolbar import debug_toolbar_urls

def root_redirect(request):             # 👈 define it here
    return redirect('/events/')

urlpatterns = [
    path('', root_redirect), 
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),  # root redirects to /events/
] #+ debug_toolbar_urls()



