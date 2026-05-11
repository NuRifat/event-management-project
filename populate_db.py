import os
import django
import random
from faker import Faker

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management_project.settings")
django.setup()

from django.contrib.auth.models import User
from events.models import Category, Event

fake = Faker()


# CREATE CATEGORIES
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


# CREATE USERS
def create_users(n=30):
    User.objects.exclude(is_superuser=True).delete()

    for _ in range(n):
        User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password="1234"
        )

    print(f"{n} Users created successfully!")


# CREATE EVENTS
def create_events(n=20):
    Event.objects.all().delete()

    categories = list(Category.objects.all())
    users = list(User.objects.filter(is_superuser=False))

    for _ in range(n):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            date=fake.date_between(start_date="-30d", end_date="+30d"),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories)
        )

        # assign random users
        assigned_users = random.sample(
            users,
            min(len(users), random.randint(1, 5))
        )

        event.participants.set(assigned_users)

    print(f"{n} Events created successfully!")


# RUN ALL
def populate():
    print("Populating database with fake data...")

    create_categories()
    create_users()
    create_events()

    print("Done! Database populated successfully.")


if __name__ == "__main__":
    populate()