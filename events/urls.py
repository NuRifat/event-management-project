from django.urls import path
from events.views import (
    create_event, organizer_dashboard, events_page, event_details, event_edit, categories, rsvp_event
)
#participants_page, create_participant, participant_details, participant_delete,

urlpatterns = [
    path('events-page', events_page, name="events-page"),
    path('organizer-dashboard', organizer_dashboard, name="organizer-dashboard"), 
    path('<int:id>/', event_details, name="event-details"),
    path('<int:id>/edit/', event_edit, name="event-edit"),
    path('event_form/', create_event, name="create-event"),
    #path('participants/', participants_page, name="participants-page"),
    #path('<int:id>/participant/', participant_details, name="participant-details"),
    #path('participant_form/', create_participant, name="create-participant"),
    #path('delete_participate/<int:id>/', participant_delete, name="delete-participant"),
    path('categories/', categories, name="categories-page"),
    path('rsvp/<int:id>/', rsvp_event, name='rsvp-event'),
]
