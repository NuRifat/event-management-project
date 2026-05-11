from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


@receiver(post_save, sender=User)
def assign_default_participant_group(sender, instance, created, **kwargs):
    if created:
        try:
            participant_group = Group.objects.get(name="Participant")
            instance.groups.add(participant_group)
        except Group.DoesNotExist:
            pass

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")

# @receiver(m2m_changed, sender=Event.participants.through)
# def send_rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
#     if action == "post_add":
#         for user_id in pk_set:
#             from django.contrib.auth.models import User
#             user = User.objects.get(pk=user_id)

#             send_mail(
#                 subject="RSVP Confirmation",
#                 message=f"You have successfully RSVP’d to {instance.name}.",
#                 from_email=None,
#                 recipient_list=[user.email],
#                 fail_silently=True,
#             )

