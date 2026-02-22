from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Category
from datetime import date, datetime
from events.forms import EventForm
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def is_participant(user):
    return user.groups.filter(name='Participant').exists()


@user_passes_test(lambda u: is_organizer(u) or is_admin(u), login_url='no-permission')
def organizer_dashboard(request):
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
    return render(request, "dashboard/organizer_dashboard.html", context)

@login_required
def events_page(request):
    query = request.GET.get("q", "").strip()

    events = Event.objects.select_related('category').prefetch_related('participants')

    if query:
        filters = Q(name__icontains=query)

        # If query looks like a date
        try:
            parsed_date = datetime.strptime(query, "%Y-%m-%d").date()
            filters |= Q(date=parsed_date)
        except:
            pass

        events = events.filter(filters)

    context = {
        "events": events,
        "query": query,
    }
    return render(request, "dashboard/events_page.html", context)


def event_details(request, id):
    event = get_object_or_404(Event, id=id)
    #If REFERER isn’t available (rare), it will fall back to events page.
    previous_url = request.META.get("HTTP_REFERER", "/events/events/")
    return render(request, "dashboard/event_details.html", {"event": event, "previous_url": previous_url})

@user_passes_test(lambda u: is_organizer(u) or is_admin(u), login_url='no-permission')
def event_edit(request, id):
    event = get_object_or_404(Event, id=id)
    
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,"Event has been Updated")
            return redirect("events-page")
    else:
        form = EventForm(instance=event)

    return render(request, "dashboard/event_edit.html", {"form": form})

@user_passes_test(lambda u: is_organizer(u) or is_admin(u), login_url='no-permission')
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Event has been Added")
            return redirect("events-page")
    else:
        form = EventForm()

    previous_url = request.META.get("HTTP_REFERER", "/events/events/")
    context = {
        "form": form,
        "previous_url": previous_url
    }
    return render(request, "dashboard/CreateEvent.html", context)

# def participants_page(request):
#     query = request.GET.get("q", "").strip()

#     participants = User.objects.prefetch_related('events')

#     if query:
#         filters = Q(name__icontains=query)
#         participants = participants.filter(filters)

#     context = {
#         "participants": participants,
#         "query": query,
#     }
#     return render(request, "dashboard/participants_page.html", context)

# def create_participant(request):
#     if request.method == "POST":
#         form = ParticipantForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Participant has been Added")
#             return redirect("participants-page")
#     else:
#         form = ParticipantForm()

#     previous_url = request.META.get("HTTP_REFERER", "/events/events/")

#     context = {
#         "form": form,
#         "previous_url": previous_url
#     }
#     return render(request, "dashboard/CreateParticipant.html", context)

# def participant_details(request, id):
#     participant = get_object_or_404(User, id=id)
#     return render(request, "dashboard/participant_details.html", {"participant": participant})

# def participant_delete(request, id):
#     participate = get_object_or_404(User, id=id)
    
#     if request.method == "POST":
#         participate.delete()
#         messages.success(request,"Participate has been Removed")
#         return redirect("participants-page")  
#     else:
#         messages.error(request,"Something went wrong")
#         return redirect("participants-page")

@login_required
def categories(request):
    categories = Category.objects.prefetch_related('event_category')
    return render(request, "dashboard/categories_page.html", {"categories":categories})


@login_required
def rsvp_event(request, id):
    event = get_object_or_404(Event, id=id)

    if event.participants.filter(id=request.user.id).exists():
        messages.warning(request, "You have already RSVP'd to this event.")
        return redirect("events-page")

    event.participants.add(request.user)

    subject = f"RSVP Confirmation - {event.name}"
    message = (
        f"Hi {request.user.username},\n\n"
        f"You have successfully RSVP'd for:\n\n"
        f"Event: {event.name}\n"
        f"Date: {event.date}\n"
        f"Time: {event.time}\n"
        f"Location: {event.location}\n\n"
        f"We look forward to seeing you!\n\n"
        f"Thank you."
    )

    send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])

    messages.success(request, "Successfully RSVP'd! A confirmation email has been sent.")
    return redirect("events-page")