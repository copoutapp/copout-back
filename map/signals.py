from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_eventstream import send_event
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token

from map.models import Event
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