from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.views import View
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from datetime import timedelta
from map.models import Event, SignupToken, Report
from map.serializers import EventSerializer, EventShortSerializer, SignupTokenSerializer, ReportSerializer

# Create your views here.


class EventListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.filter(visible=True)
        return queryset


class MyEventRecentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventShortSerializer

    def get_queryset(self):
        user = self.request.user
        # this filters into everything from two hours ago on the hour
        city = self.kwargs['city']
        this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
        two_hours_ago = this_hour - timedelta(hours=2)
        queryset_temp_event = Event.objects.filter(
            visible=True, city=city, temp=True, event_time__gt=two_hours_ago, user=user)
        queryset_permanent_event = Event.objects.filter(
            visible=True, city=city, temp=False, user=user)
        # TBD currently returning all events locations, will filter by location
        queryset = queryset_permanent_event | queryset_temp_event
        return queryset


class EventRecentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def get_queryset(self):
        # this filters into everything from two hours ago on the hour
        city = self.kwargs['city']
        this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
        two_hours_ago = this_hour - timedelta(hours=2)
        queryset_temp_event = Event.objects.filter(
            visible=True, city=city, temp=True, event_time__gt=two_hours_ago)
        queryset_permanent_event = Event.objects.filter(
            visible=True, city=city, temp=False)
        # TBD currently returning all events locations, will filter by location
        queryset = queryset_permanent_event | queryset_temp_event
        return queryset


class EventCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    # the list view is a hack to check if user is authenticated
    def get_queryset(self):
        queryset = Event.objects.none()
        return queryset


class EventDeleteView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_object(self):
        uuid = self.kwargs["uuid"]
        user = self.request.user
        result = Event.objects.get(uuid=uuid, user=user)
        return result


class SignupTokenView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupTokenSerializer

    def get_object(self):
        uuid = self.request.data["uuid"]
        result = SignupToken.objects.get(uuid=uuid, user__isnull=True)
        return result


class ReportCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')
