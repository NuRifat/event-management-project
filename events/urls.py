from django.urls import path
from events.views import (
    create_event, organizer_dashboard, events_page, event_details, event_edit,
    participants_page, create_participant, participant_details, participant_delete, categories
)

urlpatterns = [
    path('home/', organizer_dashboard, name="home-page"),  # /events/home/
    path('', events_page, name="events-page"),             # /events/
    path("<int:id>/", event_details, name="event-details"),         # /events/<id>/
    path("<int:id>/edit/", event_edit, name="event-edit"),          # /events/<id>/edit/
    path('event_form/', create_event, name="create-event"),         # /events/event_form/
    path('participants/', participants_page, name="participants-page"),  # /events/participants/
    path("<int:id>/participants/", participant_details, name="participant-details"),  # optional adjust if needed
    path("participant_form/", create_participant, name="create-participant"),
    path("delete_participate/<int:id>/", participant_delete, name="delete-participant"),
    path("categories/", categories, name="categories-page"),
]
