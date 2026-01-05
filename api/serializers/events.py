from rest_framework import serializers
from api.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "promotion", "country", "city", "venue", "date"]


class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date"]
