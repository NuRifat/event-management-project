from django import forms
from .models import Event, Participant

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "time", "location", "category"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter event name"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "rows": 4,
                "placeholder": "Write a short description"
            }),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            }),
            "time": forms.TimeInput(attrs={
                "type": "time",
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Location"
            }),
            "category": forms.Select(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            })
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter name"
            }),
            'email': forms.EmailInput(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter email"
            }),
            'events': forms.SelectMultiple(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500", 
                "multiple": "multiple",
                "size": "5",
            }),
        }
