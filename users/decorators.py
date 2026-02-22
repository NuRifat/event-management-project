from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def is_participant(user):
    return user.groups.filter(name='Participant').exists()


def admin_required(view_func):
    decorated_view = user_passes_test(is_admin)(view_func)
    return decorated_view


def organizer_required(view_func):
    decorated_view = user_passes_test(is_organizer)(view_func)
    return decorated_view


def participant_required(view_func):
    decorated_view = user_passes_test(is_participant)(view_func)
    return decorated_view
