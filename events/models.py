from django.db import models

class Category(models.Model):
    CATEGORY_CHOICES = [
        ("SCIENCE", "Science Event"),
        ("CULTURAL", "Cultural Event"),
        ("BUSINESS", "Business Event"),
        ("SPORTS", "Sports Event"),
        ("TECH", "Tech Event"),
        ("OTHER", "Other"),
    ]

    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="SCIENCE"
    )
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.get_name_display()

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="event_category")

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name="participants")

    def __str__(self):
        return self.name
