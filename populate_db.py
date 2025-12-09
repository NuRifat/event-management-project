import os
import django
import random
from faker import Faker

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management_project.settings")
django.setup()

from events.models import Category, Event, Participant   # update app name if needed

fake = Faker()

# CREATE CATEGORIES (choices)
def create_categories():
    CATEGORY_CHOICES = [
        ("SCIENCE", "Science Event"),
        ("CULTURAL", "Cultural Event"),
        ("BUSINESS", "Business Event"),
        ("SPORTS", "Sports Event"),
        ("TECH", "Tech Event"),
        ("OTHER", "Other"),
    ]

    Category.objects.all().delete()

    for value, label in CATEGORY_CHOICES:
        Category.objects.create(
            name=value,
            description=f"{label} related programs."
        )
    print("Categories created successfully!")


# CREATE EVENTS
def create_events(n=20):
    Event.objects.all().delete()

    categories = list(Category.objects.all())

    for _ in range(n):
        Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            date=fake.date_between(start_date="-30d", end_date="+30d"),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories)
        )

    print(f"{n} Events created successfully!")


# CREATE PARTICIPANTS
def create_participants(n=30):
    Participant.objects.all().delete()

    events = list(Event.objects.all())

    for _ in range(n):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )

        # Assign each participant to 1–5 random events
        assigned_events = random.sample(events, random.randint(1, 5))
        participant.events.set(assigned_events)

    print(f"{n} Participants created successfully!")


# RUN ALL
def populate():
    print("Populating database with fake data...")
    create_categories()
    create_events()
    create_participants()
    print("Done! Database populated successfully.")


if __name__ == "__main__":
    populate()
