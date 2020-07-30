from django.contrib.auth.models import User
from rest_framework import serializers
import uuid

from map.models import Event, SignupToken, Report


class EventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = [
            'uuid',
            'title',
            'event_time',
            'event_type',
            'message',
            'lat',
            'lng',
            'temp',
            'visible',
            'user',
            'city',
        ]
    # define update and create

    def create(self, validated_data):
        event = super(EventSerializer, self).create(validated_data)
        return event


class EventShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'uuid',
        ]


class UserAuthTokenRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.auth_token.key


class SignupTokenSerializer(serializers.ModelSerializer):
    user = UserAuthTokenRelatedField(read_only=True)

    class Meta:
        model = SignupToken
        fields = [
            'uuid', 'user'
        ]

    def update(self, instance, validated_data):
        if instance.user is None:
            # create new user with unusable password
            username = str(uuid.uuid4())
            user = User.objects.create(username=username)
            instance.user = user
            instance.save()
        return instance


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Report
        fields = [
            'uuid',
            'user',
            'event',
            'message',
        ]

    def create(self, validated_data):
        report = super(ReportSerializer, self).create(validated_data)
        return report
