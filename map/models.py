from django.contrib.gis.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Event(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    event_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    event_type = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    temp = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # votes = models.IntegerField(default=0)ß
    city = models.CharField(max_length=255, blank=True, null=True)


class SignupToken(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    referrer = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)


class Report(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    message = models.TextField(blank=True, null=True)
