from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_eventstream import send_event
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token

from map.models import Event, Report
from map.serializers import EventSerializer


@receiver(post_save, sender=Event)
def send_update(sender, instance, created=False, **kwargs):
    if created:
        if instance.city:
            serializer = EventSerializer(instance)
            send_event(instance.city, 'message', serializer.data)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# # UNTESTED, we want to see how the reports look before automating the banning process
# @receiver(post_save, sender=Report)
# def process_report(sender, instance, created=False, **kwargs):
#     if created:
#         reported_user = instance.event.user
#         event_reports = Report.objects.filter(event=instance.event).count()
#         total_reports = Report.objects.filter(event__user=reported_user).count()
#         # this doesn't deal with one person reporting the same events multiple times
#         # maybe count unique users amounst the reports? or unique per report?
#         if total_reports >= 100:
#             # regenerate the users token key to lock them out
#             token = Token.objects.get(user=reported_user)
#             token.key = token.generate_key()
#             token.save()
