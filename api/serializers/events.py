from rest_framework import serializers
from api.models import Event
from api.serializers.promotions import PromotionSummarySerializer


class EventSerializer(serializers.ModelSerializer):
    promotion = PromotionSummarySerializer()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "promotion",
            "country",
            "city",
            "venue",
            "date",
            "status",
        ]


class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date", "status"]
