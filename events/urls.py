from django.urls import path
from events.views import create_event, organizer_dashboard, events_page, event_details, event_edit, participants_page, create_participant, participant_details, participant_delete, categories

urlpatterns = [
    path('home/',organizer_dashboard, name="home-page"),
    path('events/',events_page, name="events-page"),
    path("events/<int:id>/", event_details, name="event-details"),
    path("events/<int:id>/edit/", event_edit, name="event-edit"),
    path('event_form/', create_event, name="create-event"),
    path('participants/', participants_page, name="participants-page"),
    path("participants/<int:id>/", participant_details, name="participant-details"),
    path("participant_form/", create_participant, name="create-participant"),
    path("delete_participate/<int:id>/", participant_delete, name="delete-participant"),
    path("categories/", categories, name="categories-page"),
]
