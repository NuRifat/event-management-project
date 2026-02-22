from django.shortcuts import render
from datetime import date, datetime
from events.models import Event, Category
from django.contrib.auth.models import User

# Create your views here.

def no_permission(request):
    return render(request, 'no_permission.html')

def home_page(request):
    type = request.GET.get('type', 'all')
    today = date.today()

    base_events = Event.objects.select_related('category').prefetch_related('participants')
    all_events = base_events
    todays_events = base_events.filter(date=today)
    upcoming = base_events.filter(date__gt=today)
    past = base_events.filter(date__lt=today)

    total_participants = User.objects.count()

    if type == "upcoming":
        events = upcoming
    elif type == "past":
        events = past
    else:
        events = all_events

    context = {
        "events": events,
        "todays_events": todays_events,
        "total_participants": total_participants,
        "total_events": all_events.count(),
        "total_upcoming": upcoming.count(),
        "total_past": past.count(),
        "type": type
    }
    return render(request, "home_page.html", context)